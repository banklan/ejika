from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Service, Review, ServiceState, Category, SubCategory, PortFolio, Testimonial, FinanceApplication, \
    EnquiryContact, PasswordReset


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields':('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'gender')}),
        (_('Permissions'), {'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields':('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(get_user_model(), CustomUserAdmin)


class InLineSubCategory(admin.TabularInline):
    model = SubCategory
    extra = 3
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'last_modified')
    prepopulated_fields = {'slug': ['name']}
    list_filter = ['name']
    search_fields = ('name',)
    inlines = [InLineSubCategory]
    list_per_page = 20
    # list_display_links = ('name', 'slug',)
    # list_editable = ('name',)

admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'last_modified')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'category']
    search_fields = ('name',)
    list_per_page = 20

admin.site.register(SubCategory, SubCategoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created', 'is_verified', 'is_featured', 'last_modified')
    prepopulated_fields = {'slug': ['title']}
    list_filter = ['created', 'subcategory', 'is_featured', 'is_verified']
    search_fields = ('title', 'owner', 'description', 'state')
    list_per_page = 20
    list_editable = ('is_verified', 'is_featured')

admin.site.register(Service, ServiceAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'is_approved', 'created',)
    list_filter = ['title', 'author', 'service']
    search_fields = ('author', 'title', 'body', 'service')
    list_editable = ('is_approved', )
    list_per_page = 20

admin.site.register(Review, ReviewAdmin)


class ServiceStateAdmin(admin.ModelAdmin):
    list_display = ('id','state',)
    prepopulated_fields = {'slug': ['state']}
    list_filter = ['state']
    search_fields = ('state',)
    list_display_links = ('id', 'state',)

admin.site.register(ServiceState, ServiceStateAdmin)


class PortFolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'service', 'is_approved', 'created')
    prepopulated_fields = {'slug': ['title']}
    list_filter = ['is_approved', 'created']
    search_fields = ('topic', 'description')
    list_display_links = ('id', 'title',)
    list_per_page = 20

admin.site.register(PortFolio, PortFolioAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'is_approved', 'is_featured', 'created')
    list_filter = ('is_approved', 'created')
    search_fields = ('name', 'company', 'text')
    list_per_page = 20
    list_editable = ('is_approved', 'is_featured')
    list_display_links = ('id', 'name',)

admin.site.register(Testimonial, TestimonialAdmin)


class FinanceApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'f_name', 'l_name', 'appliance', 'date')
    list_filter = ('date',)
    search_fields = ('email', 'f_name', 'l_name', 'appliance', 'brand')
    list_display_links = ('id', 'email',)
    list_per_page = 20

admin.site.register(FinanceApplication, FinanceApplicationAdmin)

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'f_name', 'l_name')
    search_fields = ('email', 'f_name', 'l_name', 'f_name', 'l_name')
    list_display_links = ('id', 'email',)

admin.site.register(EnquiryContact, EnquiryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('email', 'created', 'expiry')
    list_per_page = 20

admin.site.register(PasswordReset, CategoryAdmin)