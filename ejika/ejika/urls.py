from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from services.views import (
                    UserViewSets, ServiceViewSets, StatesViewSets, CategoriesViewSets,
                    ListServicesByCatAPIView, RetrieveStateAPIView, RetrieveProfileViewSet,
                    UserCreateAPIView, RetrieveAuthServiceViewSet, ProfileViewSet, UpdateProfileViewSet,
                    SubCategoriesViewSets, UpdateServiceViewSet, ServiceCreateAPIView, ServiceDelete,
                    UpdateImageAPIView, PortfolioViewSet, RelatedPortfolio, UpdatePortfolioImageViewset,
                    ReviewCreateView, ReviewViewset, ReviewUpdateView, ServiceListAPIViewSet,
                    TestimonialViewSet, FinanceApplicationViewSet, EnquiryContactViewSet,
                    PopularStates, ServicesByStateViewSet, SubCategFilterViewSets, ServicesBySubcategory,
                    UpdatePasswordView, DisableAccountViewSet, CreateTestimonialViewSet, TestimonialDelete,
                    RequestPasswordReset, VerifyTokenViewSet, ResetPasswordView
)

router = routers.DefaultRouter()
router.register('users', UserViewSets, basename='users')
router.register('services', ServiceViewSets, basename='services')
router.register('states', StatesViewSets, basename='states')
router.register('categories', CategoriesViewSets, basename='categories')
router.register('subcategories', SubCategoriesViewSets, basename="subcats")
router.register('my-profile', ProfileViewSet, basename='my-profile')
router.register('my-portfolio', PortfolioViewSet, basename='my-portfolio')
router.register(('reviews'), ReviewViewset, basename="reviews")
router.register('testimonials', TestimonialViewSet, basename="testimonials")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token, name="api-token-auth"),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/password/reset/confirm/<uidb64>/<token>/', empty_view, name='password_reset_confirm'),
    path('api/get_services_by_loc_cat/<str:loc>/<str:cat>/', ListServicesByCatAPIView.as_view(), name="get-services"),
    path('api/get_state/<str:slug>/', RetrieveStateAPIView.as_view(), name="get-state"),
    path('api/profile/', RetrieveProfileViewSet.as_view(), name="get-profile"),
    path('api/user/register/', UserCreateAPIView.as_view(), name="register"),
    path('api/auth_service/', RetrieveAuthServiceViewSet.as_view(), name="get-auth-service"),
    path('api/profile/update/', UpdateProfileViewSet.as_view(), name="update-profile"),
    path('api/update_service/', UpdateServiceViewSet.as_view(), name="update-service"),
    path('api/service/create/', ServiceCreateAPIView.as_view(), name="create-service"),
    path('api/service/delete/', ServiceDelete.as_view(), name="delete-service"),
    path('api/service/update_image/', UpdateImageAPIView.as_view(), name="update-image"),
    path('api/other-portfolio/<int:pk>/', RelatedPortfolio.as_view(), name="other-portfolio"),
    path('api/portfolio/update_image/<int:pk>/', UpdatePortfolioImageViewset.as_view(), name="update-portfolio-image"),
    path('api/review/new/<int:service>/', ReviewCreateView.as_view(), name="create-review"),
    path('api/review/update/<int:review>/', ReviewUpdateView.as_view(), name="update-review"),
    path('api/all_services', ServiceListAPIViewSet.as_view(), name="all-services"),
    path('api/send_finance_application/', FinanceApplicationViewSet.as_view(), name="send-application"),
    path('api/send_enquiry/', EnquiryContactViewSet.as_view(), name="send-enquiry"),
    path('api/popular_states/', PopularStates.as_view(), name="popular-states"),
    path('api/services_by_state/<int:state>/', ServicesByStateViewSet.as_view(), name="services-by-state"),
    path('api/get_subcategories/<str:category>/', SubCategFilterViewSets.as_view(), name="filter-by-cat"),
    path('api/services_by_subcategories', ServicesBySubcategory.as_view(), name="filter-by-subcat"),
    path('api/password-change/', UpdatePasswordView.as_view(), name="password-change"),
    path('api/disable-account/', DisableAccountViewSet.as_view(), name="disable-account"),
    path('api/send-testimonial/', CreateTestimonialViewSet.as_view(), name="send-testimonial"),
    path('api/testimonial_delete/<int:testimonial>/', TestimonialDelete.as_view(), name="del-testimonial"),
    path('api/request_password_reset/', RequestPasswordReset.as_view(), name="request-pswd-reset"),
    path('api/verify_token/<str:email>/<str:token>/', VerifyTokenViewSet.as_view(), name="reset-confirm"),
    path('api/reset_password/', ResetPasswordView.as_view(), name="password-reset"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# customise admin feel
admin.site.site_headers = 'Ejika - Administration'
admin.site.site_title = "Admin"
admin.site.index_title = 'Ejike'

