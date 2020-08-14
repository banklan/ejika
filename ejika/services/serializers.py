from datetime import datetime, timedelta
import uuid
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.text import slugify
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from .models import Service, Category, SubCategory, ServiceState, Review, CustomUser, PortFolio, Testimonial, \
    FinanceApplication, EnquiryContact, PasswordReset


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender')
    fullname = serializers.CharField(source="get_fullname")
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'fullname', 'email', 'gender', 'fullname']


class UserRegistrationSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'password', 'c_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, email):
        queryset = get_user_model().objects.filter(email=email)
        if queryset:
            raise serializers.ValidationError("A user with that email address already exists. ")
        return email

    def save(self):
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        gender = self.validated_data['gender']
        password = self.validated_data['password']
        c_password = self.validated_data['c_password']

        if len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError({'password': 'Password must be between 6 and 20 characters.'})

        if password != c_password:
            raise serializers.ValidationError({'password': 'Password and confirm password must match!'})

        user = CustomUser(first_name=first_name, last_name=last_name, email=email, gender=gender)
        user.set_password(password)
        user.save()

        # //send welcome mail
        context = {
            'data': user,
        }
        html_content = render_to_string('services/welcome.html', context)
        subject = 'Welcome to Ejika'
        message = 'Welcome to Ejika'
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        msg = EmailMultiAlternatives(subject, message, from_email,
                                     to=[to_email, from_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        Token.objects.create(user=user)


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user')


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    created = serializers.DateField(source="published_date", read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'author', 'service', 'title', 'body', 'rating', 'is_approved', 'created']
        depth = 1


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        extra_kwargs = {
            'name': {
                'validators': []
            }
        }


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'category']
        extra_kwargs = {
            'name':{
                'validators': []
            }
        }
        

class ServiceStateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ServiceState
        fields = ['id', 'state', 'slug']
        extra_kwargs = {
            'state':{
                'validators': []
            }
        }


cats = SubCategory.objects.all()


class PortfolioSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None)
    slug = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(source="published", read_only=True)
    author = UserSerializer(read_only=True)
    class Meta:
        model = PortFolio
        fields = ['id', 'title', 'description', 'slug', 'image', 'is_approved', 'created', 'cost', 'author']

    def create(self, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        cost = validated_data.get('cost')
        image = validated_data.get('image', None)
        author = self.context['request'].user
        service = Service.objects.get(owner=author)
        slug = slugify(title)
        portfolio = PortFolio.objects.create(title=title, description=description, cost=cost, image=image, service=service, slug=slug, author=author)
        return portfolio

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.slug = slugify(instance.title)
        instance.save()
        return instance


class ServiceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    created = serializers.DateField(source="published_date", read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    ratings = serializers.DecimalField(max_digits=2, decimal_places=1, source="rating_average", read_only=True)
    image =serializers.SerializerMethodField()
    subcategory = SubCategorySerializer(read_only=False)
    state = ServiceStateSerializer(read_only=False)
    slug = serializers.CharField(read_only=True)
    portfolio = PortfolioSerializer(many=True, read_only=True)
    website = serializers.URLField()

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'owner', 'slug', 'subcategory', 'is_featured', 'is_verified', 'view_count',
                  'street_address', 'city', 'state', 'phone_number', 'ratings', 'reviews', 'portfolio', 'image', 'created',
                  'website', 'fb', 'instag']

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_image())

    def update(self, instance, validated_data):
        state_data = validated_data.pop('state')
        subcategory_data = validated_data.pop('subcategory')
        instance.title = validated_data.get('title', instance.title)
        instance.description  = validated_data.get('description', instance.description)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        instance.city = validated_data.get('city', instance.city)
        instance.website = validated_data.get('website', instance.website)
        instance.fb = validated_data.get('fb', instance.fb)
        instance.instag = validated_data.get('instag', instance.instag)

        state_id = state_data.get('id', None)
        if(state_id):
            instance.state = ServiceState.objects.get(id=state_id)
            instance.state.id = state_data.get('id', instance.state.id)
            instance.state.state = state_data.get('state', instance.state.state)
            instance.state.slug = state_data.get('slug', instance.state.slug)
            instance.state.save()

        subcategory_id = subcategory_data.get('id', None)
        if(subcategory_id):
            instance.subcategory = SubCategory.objects.get(id=subcategory_id)
            instance.subcategory.id = subcategory_data.get('id', instance.subcategory.id)
            instance.subcategory.name = subcategory_data.get('name', instance.subcategory.name)
            instance.subcategory.slug = subcategory_data.get('slug', instance.subcategory.slug)
            instance.subcategory.save()

        instance.save()
        return instance

    def create(self, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        street_address = validated_data.get('street_address')
        city = validated_data.get('city')
        phone_number = validated_data.get('phone_number')
        slug = slugify(title)
        image = validated_data.get('image', None)
        website = validated_data.get('website')
        fb = validated_data.get('fb')
        instag = validated_data.get('instag')
        state_data = validated_data.pop('state')

        state_id = state_data.get('id')
        if state_id:
            state = ServiceState.objects.get(id=state_id)

        subcategory_data = validated_data.pop('subcategory')
        subcat_id = subcategory_data.get('id')
        if subcat_id:
            subcategory = SubCategory.objects.get(id=subcat_id)

        service = Service.objects.create(title=title, description=description, street_address=street_address, city=city,
                                         state=state, subcategory=subcategory, phone_number=phone_number, slug=slug,
                                         image=image, website=website, fb=fb, instag=instag, owner=self.context['request'].user)
        return service


class ServiceImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None)
    class Meta:
        model = Service
        fields = ['image']

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class PortFolioImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None)
    class Meta:
        model = PortFolio
        fields = ['image']

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image')
        instance.save()
        return instance


class CreateReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    created = serializers.DateTimeField(source="published_date", read_only=True)
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'title', 'body', 'author', 'rating', 'is_approved', 'created', 'service']
        depth = 1

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.body = validated_data.get('body')
        instance.rating = validated_data.get('rating')
        instance.save()
        return instance


class TestimonialSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source="published", read_only=True)
    image = serializers.ImageField(max_length=None)
    user = serializers.IntegerField()

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'company', 'text', 'email', 'address', 'position', 'is_approved', 'user', 'is_featured', 'created', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_image())

    def create(self, validated_data):
        name = validated_data.get('name')
        company =  validated_data.get('company')
        address = validated_data.get('address')
        email = validated_data.get('email')
        position = validated_data.get('position')
        user = validated_data.get('user', None)
        text =validated_data.get('text')
        image = validated_data.get('image', None)
        test = Testimonial.objects.create(name=name, company=company, address=address, email=email, position=position, user=user, text=text, image=image)
        return test


class FinanceApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceApplication
        fields = ['id', 'title', 'f_name', 'l_name', 'phone', 'email', 'occupation', 'brand', 'appliance', 'capacity', 'other_info',
                  'income', 'frequency', 'tenure', 'location', 'res_address', 'bus_address', 'mode_of_repymt', 'guarantor_name',
                  'guarantor_address', 'guarantor_phone', 'date']

    def create(self, validated_data):
        application = super(FinanceApplicationSerializer, self).create(validated_data)
        subject = 'Application for appliance financing'
        message = 'Application sent by: {}'.format(validated_data.get('f_name'))
        sender = validated_data.get('email')
        to_email = 'vidspectra20@gmail.com'
        app = FinanceApplication(**validated_data)
        context = {
            'data': app
        }
        html_content = render_to_string('services/app_rcvd.html', context)

        # //send message to ejika
        msg = EmailMultiAlternatives(subject=subject, body=message, from_email=sender,
                                     to=[to_email, settings.EMAIL_HOST_USER])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # send message to customer
        sender = 'vidspectra20@gmail.com'
        client = validated_data.get('email')
        html_cont_client = render_to_string('services/app_sent.html', context)
        messg = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=[app.email])
        messg.attach_alternative(html_cont_client, "text/html")
        messg.send()
        return application


class EnquiryContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = EnquiryContact
        fields = ['email', 'f_name', 'l_name', 'phone', 'subject', 'message']

    def create(self, validated_data):
        from_email = validated_data.get('email')
        f_name = validated_data.get('f_name')
        l_name = validated_data.get('l_name')
        phone = validated_data.get('phone')
        subject = 'Enquiry: ' + validated_data.get('subject')
        message = validated_data.get('message')
        application = super(EnquiryContactSerializer, self).create(validated_data)
        to_email = 'vidspectra20@gmail.com'
        app = EnquiryContact(**validated_data)
        context = {
            'data': app,
        }
        html_content = render_to_string('services/enquiry.html', context)

        # //send message to ejika
        msg = EmailMultiAlternatives(subject, message, from_email,
                                     to=[to_email, settings.EMAIL_HOST_USER])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return application


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['password']


class DisableAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['is_active']


class PasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField
    class Meta:
        model = PasswordReset
        fields = ['email', 'token', 'created']

    def create(self, validated_data):
        email = validated_data.get('email')
        user = get_user_model().objects.get(email=email)
        if user:
            # token = uuid.uuid4()
            token = secrets.token_hex(88)
            expiry = datetime.now() + timedelta(hours=1)
            entry = PasswordReset.objects.create(email=email, token=token, expiry=expiry)
            # send email
            frontend = 'http://localhost:8080/password_reset/{}/{}'.format(email, token)
            context = {
                'user': user.first_name,
                'email': email,
                'token': token,
                'frontend': frontend
            }
            subject = 'Password Reset Request On Ejika'
            message = 'Password reset on ejika.com'
            to_email = user.email
            html_content = render_to_string('services/password_reset_enquiry.html', context)
            msg = EmailMultiAlternatives(subject, message, from_email=settings.EMAIL_HOST_USER,
                                             to=[to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return entry
        raise serializers.ValidationError("User with that email doesn't exist in our database.")


class ResetUserPasswordSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'c_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        token = self.validated_data['token']
        req = PasswordReset.objects.get(token=token)
        email = req.email
        user = get_user_model().objects.get(email=email)

        password = self.validated_data['password']
        c_password = self.validated_data['c_password']

        if len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError({'password': 'Password must be between 6 and 20 characters.'})

        if password != c_password:
            raise serializers.ValidationError({'password': 'Password and confirm password must match!'})
            user.set_password(password)
            user.save()
            return user

