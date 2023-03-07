from . import models
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    message = serializers.SerializerMethodField()

    class Meta:
        model = models.Message
        fields = ["from_user", "to_user", "message", "created"]

    def get_from_user(self, obj):
        return {
            "name": obj.from_user.username,
            "dp": obj.from_user.dp.url,
            "pk": obj.from_user.pk,
        }

    def get_to_user(self, obj):
        return {
            "name": obj.to_user.username,
            "dp": obj.to_user.dp.url,
            "pk": obj.to_user.pk,
        }

    def get_message(self, obj):
        return obj.message or "sent an image"
