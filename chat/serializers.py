from . import models
from rest_framework import serializers
from authn.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):

    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = models.Message
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    def get_recent_message(self, obj):
        return MessageSerializer(obj.messages.all().order_by("-created").first()).data

    recent_message = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = models.Chat
        fields = "__all__"


class KeyRingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeyRing
        fields = "__all__"
