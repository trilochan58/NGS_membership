from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """using custom forms in django admin panel to create and edit users"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "id",
        "email",
        "full_name",
        "role",
        "is_verified",
        "is_superuser",
    )
    list_filter = (
        "email",
        "role",
        "is_verified",
        "is_superuser",
    )

    """for showing fields we want in admin panel"""
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "phone",
                    "role",
                    "token",
                    "is_verified",
                )
            },
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
    )

    """for adding fields we want when creating user from admin panel"""
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone",
                    "role",
                    "token",
                    "is_verified",
                )
            },
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
    )
    search_fields = ("email",)
    ordering = ("-id",)


admin.site.register(CustomUser, CustomUserAdmin)
