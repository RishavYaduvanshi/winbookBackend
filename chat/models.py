from django.db import models
from django.conf import settings


class Chat(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chats",
    )

    name = models.CharField(max_length=255, blank=False)

    dp = models.ImageField(
        upload_to="chat/dp",
        blank=True,
        default="../static/authn/dp.png",
    )

    is_group = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Message(models.Model):

    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.TextField(blank=True)

    chat = models.ForeignKey(
        Chat, related_name="messages", on_delete=models.CASCADE, blank=True, null=True
    )

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created"]


class KeyRing(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="keyring", on_delete=models.CASCADE
    )
    public_key = models.TextField()
    private_key_enc = models.TextField()

    password_hash = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.username}'s keyring"
