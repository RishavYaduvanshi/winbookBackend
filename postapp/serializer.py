from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Post, Comment


class CommentSerializer(ModelSerializer):
    def __init__(self, write=False, *args, **kwargs):
        if write == False:
            self.post = SerializerMethodField()
            self.user = SerializerMethodField()
        super().__init__(*args, **kwargs)

    def get_post(self, obj):
        return obj.post.pk

    def set_post(self, obj):
        return obj.post.pk

    def get_user(self, obj):
        return obj.user.pk

    class Meta:
        model = Comment
        fields = (
            "user",
            "post",
            "comment",
            "created_at",
            "replies",
            "pk",
            "replied_to",
        )
        read_only_fields = ("created_at",)
        extra_kwargs = {
            "comment": {"required": True},
            "replied_to": {"write_only": True},
            "replies":{"read_only":True},
        }


class PostSerializer(ModelSerializer):
    def get_userName(self, obj):
        return str(obj.user.username)

    def get_userDp(self, obj):
        return self.context["request"].build_absolute_uri("/media/" + str(obj.user.dp))

    userName = SerializerMethodField()
    userDp = SerializerMethodField()
    liked_cnt = SerializerMethodField()
    likedStatus = SerializerMethodField()
    # user = SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.pk

    def get_liked_cnt(self, obj):
        return obj.liked_by.count()

    def get_likedStatus(self, obj):
        return obj.liked_by.filter(pk=self.context["request"].user.pk).exists()

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post

        fields = (
            "url",
            "caption",
            "liked_cnt",
            "created_at",
            "updated_at",
            "pk",
            "userName",
            "user",
            "likedStatus",
            "userDp",
            "comments",
        )
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "url": {"required": True},
            "caption": {"required": True},
        }
