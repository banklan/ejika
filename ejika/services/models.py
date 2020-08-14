import secrets

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# custom user
from django_resized import ResizedImageField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be entered.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff set to True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser set to True')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(choices=GENDER, max_length=2, default='M')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name =('user')
        verbose_name_plural = ('users')

    def get_gender(self):
        if self.gender == 'F':
            return 'Female'
        return 'Male'

    def get_fullname(self):
        return self.first_name + ' ' + self.last_name


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# create a slug while saving model
def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_category_slug, sender=Category)


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# create a slug while saving model
def pre_save_subcategory_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_subcategory_slug, sender=SubCategory)


class ServiceState(models.Model):
    state = models.CharField(max_length=20, unique=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state

    class Meta:
        ordering = ['state']


# create slug from state while saving model
def pre_save_state_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.state)


# connect signal to mode;
pre_save.connect(pre_save_state_slug, sender=ServiceState)


class Service(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(max_length=2000, null=False, blank=False)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    street_address = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.ForeignKey(ServiceState, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    fb = models.CharField(max_length=100, blank=True, null=True)
    instag = models.CharField(max_length=100, blank=True, null=True)
    image = ResizedImageField(size=[520, 400], quality=85, upload_to="images/profiles", blank=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def published_date(self):
        pub = self.created
        mod = pub.strftime("%B %d, %Y")
        return mod

    def rating_average(self):
        total = 0
        reviews = Review.objects.filter(service=self)
        for review in reviews:
            total = total + review.rating
        if len(reviews) > 0:
            return int(round(total / len(reviews)))
        else:
            return 0

    def incrementViewCount(self):
        self.view_count += 1
        self.save()

    def fullname(self):
        return self.owner.first_name +' ' + self.owner.last_name

    def portfolio(self):
        portfolio = PortFolio.objects.filter(service=self)
        return portfolio

    @property
    def reviews(self):
        return self.review_set.all()

    def get_image(self):
        if self.image:
            return self.image.url
        return settings.MEDIA_URL + 'images/profiles/no-image.png'


@receiver(pre_delete, sender=Service)
def service_delete(sender, instance, **kwargs):
    instance.image.delete(False)


# create slug from username and title of service while saving model
def pre_save_service_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.owner__email + '-' + instance.title)


# connect signal to model;
pre_save.connect(pre_save_service_slug, sender=Service)


class Review(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False, null=False)
    body = models.TextField(max_length=400, blank=False, null=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def published_date(self):
        pub = self.created
        mod = pub.strftime("%B %d, %Y, %I:%M %p")
        return mod

    class Meta:
        ordering = ['-created']


class PortFolio(models.Model):
    service = models.ForeignKey(Service, related_name="service", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=400)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = ResizedImageField(size=[520, 400], quality=85, upload_to='images/portfolio', default='images/portfolio/no-image.png', null=False, blank=False)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def published(self):
        pub = self.created
        mod = pub.strftime("%B %d, %Y")
        return mod


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField()
    position = models.CharField(max_length=30, null=True)
    user = models.IntegerField(null=True, blank=True)
    text = models.TextField(max_length=300)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    image = ResizedImageField(size=[400, 400], quality=85, upload_to="images/testimonials", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def published(self):
        pub = self.created
        mod = pub.strftime("%B %d, %Y")
        return mod

    class Meta:
        ordering = ['-created']

    def get_image(self):
        if self.image:
            return self.image.url
        return settings.MEDIA_URL + 'images/testimonials/no-image.png'


class FinanceApplication(models.Model):
    title = models.CharField(max_length=10, null=True, blank=True)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    phone = models.IntegerField()
    occupation = models.CharField(max_length=50)
    brand = models.CharField(max_length=20)
    appliance = models.CharField(max_length=50)
    capacity = models.CharField(max_length=20)
    other_info = models.TextField(max_length=150, blank=True, null=True)
    income =  models.DecimalField(decimal_places=2, max_digits=10)
    tenure = models.CharField(max_length=10)
    frequency = models.CharField(max_length=15)
    location = models.CharField(max_length=40)
    res_address = models.TextField(max_length=300, blank=True, null=True)
    bus_address = models.TextField(max_length=300, blank=True, null=True)
    mode_of_repymt = models.CharField(max_length=100, blank=True, null=True)
    guarantor_name = models.CharField(max_length=200, blank=True, null=True)
    guarantor_address = models.CharField(max_length=200, blank=True, null=True)
    guarantor_phone = models.CharField(max_length=16, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-date']

    def appl_date(self):
        pub = self.date
        mod = pub.strftime("%B %d, %Y, %I:%M %p")
        return mod


class EnquiryContact(models.Model):
    email = models.EmailField()
    f_name = models.CharField(max_length=30, blank=True, null=True)
    l_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.email


class PasswordReset(models.Model):
    email = models.EmailField(null=True)
    token = models.CharField(max_length=200, default=secrets.token_hex(88))
    expiry = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

