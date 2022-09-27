from django.contrib import admin
from .models import Post, Comment

# Register your models here.


admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "comment",
        "created_at",
    )
    list_filter = ("user", "post", "created_at")
    search_fields = ("user", "post", "comment")
