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

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Chat
        fields = "__all__"


class KeyRingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeyRing
        fields = "__all__"
