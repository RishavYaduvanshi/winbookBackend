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
    def get_dp(self, obj):
        return (
            obj.dp.url
            if obj.is_group
            else obj.users.exclude(id=self.context["request"].user.id).first().dp.url
        )

    messages = MessageSerializer(many=True, read_only=True)
    dp = serializers.SerializerMethodField()

    class Meta:
        model = models.Chat
        fields = "__all__"


class KeyRingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeyRing
        fields = "__all__"
