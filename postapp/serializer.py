from rest_framework.serializers import ModelSerializer,SerializerMethodField

from .models import Post

class PostSerializer(ModelSerializer):
    
    def get_userName(self, obj):
        return str(obj.user.username)
    
    def get_userDp(self, obj):
        return self.context['request'].build_absolute_uri('/media/'+str(obj.user.dp))


    userName = SerializerMethodField()
    userDp = SerializerMethodField()
    liked_cnt = SerializerMethodField()
    likedStatus = SerializerMethodField()
    

    def get_liked_cnt(self, obj):
        return obj.liked_by.count()
    
    def get_likedStatus(self, obj):
        return obj.liked_by.filter(pk=self.context['request'].user.pk).exists()
    
    
    class Meta:
        model = Post
        
        fields = ('url', 'caption', 'liked_cnt', 'created_at', 'updated_at','pk', 'userName','user','likedStatus','userDp')
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'url': {'required': True},
            'caption': {'required': True},
        }

    