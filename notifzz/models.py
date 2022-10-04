from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    date = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="notifications"
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="actor",
        parent_link=False,
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        "postapp.Post",
        on_delete=models.CASCADE,
        related_name="post",
        parent_link=False,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date"]
