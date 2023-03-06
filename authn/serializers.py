from .models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from postapp.serializer import PostSerializer


class UserSerializer(ModelSerializer):
    posts = PostSerializer(
        many=True,
        read_only=True,
    )  # source="posts")
    follower_count = SerializerMethodField()
    following_count = SerializerMethodField()
    following = SerializerMethodField()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return None
        return user.following.filter(pk=obj.pk).exists()

    class Meta:
        model = User
        exclude = ("password", "followers", "blocked_users")
        depth = 0
