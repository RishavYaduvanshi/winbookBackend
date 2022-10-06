from django.db import models
from django.dispatch import Signal
from django.conf import settings
from uuid import uuid4
from . import signals


class Post(models.Model):
    POST_CREATED = "create"
    POST_LIKED = "like"
    POST_UNLIKED = "unlike"

    user = models.ForeignKey("authn.User", on_delete=models.CASCADE)
    post_id = models.UUIDField(default=uuid4, null=True, blank=True)
    url = models.ImageField(upload_to="posts/", null=True, blank=True)
    caption = models.TextField(default="", null=True, blank=True)
    liked_by = models.ManyToManyField("authn.User", related_name="likes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at", "-updated_at", "-pk"]
        constraints = [
            models.CheckConstraint(
                check=~(models.Q(caption__exact="") & models.Q(url__exact="")),
                name="url_or_caption",
                violation_error_message="Post must have atleast a url or a caption",
            )
        ]

    def like(self, user):
        try:
            if not self.liked_by.filter(pk=user.pk).exists():
                self.liked_by.add(user)
                self.likes_count += 1
                self.save()
                signals.post_signal.send_robust(
                    self.__class__, instance=self, user=user, action=self.POST_LIKED
                )
            return True
        except:
            return False

    def unlike(self, user):
        try:
            if self.liked_by.filter(pk=user.pk).exists():
                self.liked_by.remove(user)
                self.likes_count -= 1
                self.save()
                Signal.send_robust(
                    self.__class__, instance=self, user=user, action=self.POST_UNLIKED
                )
            return True
        except:
            return False

    def toggle_like(self, user):
        if self.liked_by.filter(pk=user.pk).exists():
            return self.unlike(user)
        return self.like(user)

    def save(self, *args, **kwargs):
        new_post = self._state.adding
        s = super().save(*args, **kwargs)
        if new_post:
            print("Post created")
            signals.post_signal.send_robust(
                self.__class__, instance=self, user=self.user, action=self.POST_CREATED
            )
        return s


class Comment(models.Model):
    COMMENT_CREATED = "create"
    COMMENT_UPDATED = "update"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(post__isnull=True) | models.Q(replied_to__isnull=True))
                    & (
                        models.Q(post__isnull=False)
                        | models.Q(replied_to__isnull=False)
                    )
                ),
                name="post_xor_replied_to",
                violation_error_message="Comment must be either a reply or a post comment, not Both",
            ),
        ]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        s = super().save(*args, **kwargs)
        if is_new:
            signals.comment_signal.send_robust(
                self.__class__,
                instance=self,
                user=self.user,
                action=self.COMMENT_CREATED,
            )
        else:
            signals.comment_signal.send_robust(
                self.__class__, instance=self, action=self.COMMENT_UPDATED
            )

        return s
