from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date", "isRead", "users", "actor", "post")

    def users(self, obj):
        if obj.users.count() > 3:
            return (
                ",".join(
                    obj.users.only("username")[:3].values_list("username", flat=True)
                )
                + "..."
            )
