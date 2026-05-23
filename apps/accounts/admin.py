from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("last_name", "first_name", "email", "is_staff", "is_active")
    list_display = (
        "email", "first_name", "last_name", "phone_number", "is_staff", "is_active"
    )

    fieldsets = (
        ("Login", {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "phone_number", "date_of_birth")
        }
         ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "date_of_birth",
                "password1",
                "password2",
                "is_active",
            ),
        }),
    )

    search_fields = ("email", "first_name", "last_name", "date_of_birth")
