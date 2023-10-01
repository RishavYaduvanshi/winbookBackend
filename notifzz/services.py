from rest_framework import serializers
from . import models
from push_notifications.models import GCMDevice


def send_notification(instance):
    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Notification
            exclude = ["users"]

    notification_data = NotificationSerializer(instance).data
    
    desc = notification_data.pop("description")
    for user in instance.users.all():
        devices = GCMDevice.objects.filter(user=user)
        devices.send_message(desc, extra=notification_data)
