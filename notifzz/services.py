from rest_framework import serializers
from . import models
from push_notifications.models import GCMDevice


def send_notification(instance):
    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Notification
            exclude = ["users"]

    d = NotificationSerializer(instance).data
    print(d)
    print(instance.users.all())
    desc = d.pop("description")
    for user in instance.users.all():
        devices = GCMDevice.objects.filter(user=user)
        print(devices)
        devices.send_message(desc, extra=d)
