from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_active", "is_staff", "is_superuser", "is_verified")
    search_fields = ("email", "username", "is_active", "is_staff", "is_superuser",)
    list_filter = ("is_active", "is_staff", "is_superuser", "is_verified")
    filter_horizontal = ()
    ordering = ("email",)
    fieldsets = (
        ("Personal", {'fields': ('username', 'email', 'password')}),
        ("Permissions", {"fields": ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ("dates", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ("Personal Info", {"fields": ('username', 'email', '<PASSWORD>', '<PASSWORD>')}),
        ("Permissions",  {'fields': ("is_active", "is_staff", "is_superuser", "is_verified")},)
    )


admin.site.register(CustomUser, UserAdmin)
