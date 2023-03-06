from . import models
from rest_framework import serializers
from authn.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):

    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = models.Message
        fields = "__all__"
