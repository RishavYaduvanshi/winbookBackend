from django.db import models
from django.conf import settings


class Message(models.Model):

    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.TextField(blank=True)

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.pk}. {self.from_user} to {self.to_user}"

    # class Meta:
    #     ordering = ["-created"]
