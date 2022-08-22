from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'caption', 'liked_by', 'created_at', 'updated_at','pk')
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'url': {'required': True},
            'caption': {'required': True},
        }
    