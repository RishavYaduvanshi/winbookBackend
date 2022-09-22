from .models import User
from rest_framework.serializers import ModelSerializer
from postapp.serializer import PostSerializer
class UserSerializer(ModelSerializer):
    posts = PostSerializer(many=True, read_only=True, source='post_set')
    class Meta:
        model = User
        exclude = ('password',)