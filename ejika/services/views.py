from datetime import datetime, timedelta
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import viewsets, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Service, ServiceState, Category, CustomUser, SubCategory, PortFolio, Review, Testimonial, \
    FinanceApplication, EnquiryContact, PasswordReset
from .serializers import UserSerializer, ServiceSerializer, ServiceStateSerializer, UserRegistrationSerializer, \
    CategorySerializer, SubCategorySerializer, ServiceImageSerializer, PortfolioSerializer, PortFolioImageSerializer, \
    ReviewSerializer, CreateReviewSerializer, TestimonialSerializer, FinanceApplicationSerializer, \
    EnquiryContactSerializer, ChangePasswordSerializer, DisableAccountSerializer, \
    PasswordRequestSerializer
from .pagination import ServiceListPagination


class UserViewSets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    authentication_classes = [TokenAuthentication, ]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status': 'success',
            'message': 'Your registration was successful. Thank you.',
            'resp': status.HTTP_201_CREATED
        }
        return Response(response)


class ServiceViewSets(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_object(self):
        item = super(ServiceViewSets, self).get_object()
        item.incrementViewCount()
        return item


class ServiceListAPIViewSet(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = ServiceListPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('state__slug', 'subcategory__category__slug')
    search_fields = ['title', 'description', 'owner__first_name', 'owner__last_name']


class StatesViewSets(viewsets.ModelViewSet):
    serializer_class = ServiceStateSerializer
    queryset = ServiceState.objects.all()
    permission_classes = [AllowAny,]


class CategoriesViewSets(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny,]


class SubCategoriesViewSets(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = [AllowAny,]


class ListServicesByCatAPIView(ListAPIView):
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        loc = kwargs.get('loc')
        cat = kwargs.get('cat')
        queryset = Service.objects.filter(subcategory__category__slug=cat, state__slug=loc)
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class RetrieveStateAPIView(RetrieveAPIView):
    queryset = ServiceState.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().get(slug=self.kwargs.get('slug'))
        serializer = ServiceStateSerializer(queryset)
        return Response(serializer.data)


class RetrieveProfileViewSet(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def retrieve(self, request, *args, **kwargs):
        user = request.user.id
        queryset = self.get_queryset().get(id=user)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class RetrieveAuthServiceViewSet(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        user = self.request.user
        service = self.get_queryset().get(owner=user)
        return service

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        try:
            instance = self.get_queryset().get(owner=user)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Service.DoesNotExist:
            res = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Service does not exist',
            }
            return Response(res)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        profile = get_user_model().objects.get(id=self.request.user.id)
        return profile


class UpdateProfileViewSet(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        profile = get_user_model().objects.get(id=self.request.user.id)
        return profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UpdateServiceViewSet(UpdateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        service = Service.objects.get(owner=self.request.user)
        return service


class ServiceCreateAPIView(CreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def create(self, request, *args, **kwargs):
        context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {'message': 'Service created!', 'result': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(created=timezone.now())


class ServiceDelete(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceState
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        service = self.get_queryset().get(owner=self.request.user)
        return service

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateImageAPIView(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        service = self.get_queryset().get(owner=self.request.user)
        return service

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image is None:
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            instance.image.delete()
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = PortFolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RelatedPortfolio(ListAPIView):
    queryset = PortFolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def list(self, request, *args, **kwargs):
        portfolio = PortFolio.objects.get(id=self.kwargs['pk'])
        queryset = PortFolio.objects.filter(service=portfolio.service).exclude(id=self.kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class UpdatePortfolioImageViewset(UpdateAPIView):
    queryset = PortFolio.objects.all()
    serializer_class = PortFolioImageSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('pk')
        portfolio = self.get_queryset().get(id=id)
        return portfolio

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image is not None:
            instance.image.delete()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk')
        instance = self.get_queryset().filter(id=id)
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewCreateView(CreateAPIView):
    serializer_class = CreateReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        service = Service.objects.get(id=self.kwargs.get('service'))
        return service

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = self.request.user
        service_id = kwargs.get('service')
        service = Service.objects.get(id=service_id)
        serializer.save(service=service, author=author)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewUpdateView(UpdateAPIView):
    serializer_class = CreateReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('review')
        instance = Review.objects.get(id=id)
        return instance

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()

    def get_queryset(self):
        testis = Testimonial.objects.filter(is_featured=True)
        return testis


class CreateTestimonialViewSet(CreateAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Application submitted!', 'result': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)


class TestimonialDelete(DestroyAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('testimonial')
        instance = self.get_queryset().get(id=id)
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FinanceApplicationViewSet(CreateAPIView):
    serializer_class = FinanceApplicationSerializer
    queryset = FinanceApplication.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Application submitted!', 'result': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)


class EnquiryContactViewSet(CreateAPIView):
    serializer_class = EnquiryContactSerializer
    queryset = EnquiryContact.objects.all()

    # @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Enquiry Sent!', 'result': serializer.data}
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class PopularStates(ListAPIView):
    serializer_class = ServiceStateSerializer

    def list(self, request, *args, **kwargs):
        locs_list = [10, 37, 18, 19, 38, 27, 30, 32, 29, 4, 12]
        queryset = ServiceState.objects.filter(id__in=locs_list)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServicesByStateViewSet(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = ServiceListPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('state__slug', 'subcategory__category__slug')
    search_fields = ['title', 'description', 'owner__first_name', 'owner__last_name']

    def get_queryset(self):
        queryset = Service.objects.filter(state__id=self.kwargs.get('state'))
        return queryset


class SubCategFilterViewSets(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = SubCategory.objects.filter(category__slug=self.kwargs.get('category'))
        return queryset


class ServicesBySubcategory(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = ServiceListPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('state__slug', 'subcategory__slug')


class UpdatePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check old password
            if not instance.check_password(serializer.data.get('password')):
                return Response({'status': 'failed', 'message': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('confirm_password') != request.data.get('new_password'):
                raise serializer.ValidationError({'password': 'New password and Confirm password must match'})

            # if everything is ok
            instance.set_password(request.data.get('new_password'))
            instance.save()
            update_session_auth_hash(request, instance)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DisableAccountViewSet(UpdateAPIView):
    serializer_class = DisableAccountSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.is_active = False
        serializer.save()
        return Response(serializer.data)


class RequestPasswordReset(CreateAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Password request mail Sent!', 'result': serializer.data}
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class VerifyTokenViewSet(RetrieveAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordRequestSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_queryset().get(token=kwargs.get('token'), email=kwargs.get('email'))
        if obj:
            if obj.expiry > datetime.now():
                serializer = self.get_serializer(obj)
                response = {'message': 'ok', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            res = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Token has expired',
            }
            return Response(res)
        res = {
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'User does not exist on our database',
        }
        return Response(res)


class ResetPasswordView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        token = self.request.data['token']
        req = PasswordReset.objects.get(token=token)
        obj = self.get_queryset().get(email=req.email)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check old password
            if len(request.data.get('password')) < 6 or len(request.data.get('password')) > 20:
                raise serializer.ValidationError({'password' : 'Password must not be less than 5 characters long and must not be more than 20 characters long.'})

            if request.data.get('c_password') != request.data.get('password'):
                raise serializer.ValidationError({'password': 'New password and Confirm password must match'})

            # if everything is ok
            instance.set_password(request.data.get('password'))
            instance.save()
            update_session_auth_hash(request, instance)

            # delete the password reset entry from db
            token = request.data['token']
            req = PasswordReset.objects.get(token=token)
            req.delete()

            context = {
                'user': instance.first_name,
            }

            # send email to notify password was reset
            subject = 'Your Password Has Been Reset'
            message = 'Password reset successfully on ejika.com'
            to_email = instance.email
            html_content = render_to_string('services/password_reset_success.html', context)
            msg = EmailMultiAlternatives(subject, message, from_email=settings.EMAIL_HOST_USER,
                                         to=[to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


