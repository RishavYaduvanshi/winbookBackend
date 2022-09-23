from django.db import models
from django.dispatch import Signal


class Post(models.Model):
    POST_CREATED = "create"
    POST_LIKED = "like"
    POST_UNLIKED = "unlike"

    user = models.ForeignKey("authn.User", on_delete=models.CASCADE)
    url = models.ImageField(upload_to="posts/")
    caption = models.CharField(max_length=200)
    liked_by = models.ManyToManyField("authn.User", related_name="likes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at", "-updated_at", "-pk"]

    def like(self, user):
        try:
            if not self.liked_by.filter(pk=user.pk).exists():
                self.liked_by.add(user)
                self.likes_count += 1
                self.save()
                Signal.send_robust(
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
        super().save(*args, **kwargs)
        if self._state.adding:
            Signal.send_robust(
                self.__class__, instance=self, user=self.user, action=self.POST_CREATED
            )
