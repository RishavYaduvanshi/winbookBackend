from django.db import models
from django.conf import settings


class Chat(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chats",
    )
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-pk"]
        # same users in different order are the same chat
        constraints = [
            models.UniqueConstraint(
                fields=["users"], name="unique_users", condition=models.Q(name="")
            )
        ]

    def __str__(self):
        if self.name:
            return self.name
        users = self.users.all()
        count = users.count()
        if count == 2:
            return f"{users[0].username} and {users[1].username}"
        return f"{self.pk} {users[0].username} and {count - 1} others"


class Message(models.Model):

    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.TextField(blank=True)

    chat = models.ForeignKey(
        Chat, related_name="messages", on_delete=models.CASCADE, blank=True, null=True
    )

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE
    )

    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created", "read"]


class KeyRing(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="keyring", on_delete=models.CASCADE
    )
    public_key = models.TextField()
    private_key_enc = models.TextField()

    password_hash = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.username}'s keyring"
