from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.admin import _

# Register your models here.


@admin.register(User)
class UserAdmin(_UserAdmin):
    fieldsets = _UserAdmin.fieldsets + (
        (
            _("Social"),
            {
                "fields": (
                    "bio",
                    "dp",
                    "cover",
                    "followers",
                    "following",
                    "private_account",
                    "blocked_users",
                )
            },
        ),
    )
