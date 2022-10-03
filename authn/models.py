from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser as _User
from django.dispatch import Signal
from uuid import uuid4

# Create your models here.
class User(_User):
    class Meta:
        ordering = ("-date_joined",)

    bio = models.TextField(blank=True, default="Add Bio", null=True)
    user_id = models.UUIDField(default=uuid4, null=True, blank=True)
    dp = models.ImageField(
        upload_to="dp/",
        blank=True,
        default="../static/authn/dp.png",
    )

    cover = models.ImageField(
        upload_to="covers/",
        blank=True,
        default="../static/authn/cover.png",
    )

    followers = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="follows",
    )

    following = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="followed_by",
    )

    blocked_users = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="blocked_by",
    )

    private_account = models.BooleanField(default=False)

    def follow(self, user):
        try:
            self.following.add(user)
            user.followers.add(self)
            self.save()
            user.save()
            Signal.send_robust(
                self.__class__, instance=self, user=user, action="follow"
            )
            return True
        except:
            return False

    def unfollow(self, user):
        try:
            self.following.remove(user)
            user.followers.remove(self)
            self.save()
            user.save()
            Signal.send_robust(
                self.__class__, instance=self, user=user, action="unfollow"
            )
            return True
        except:
            return False

    def remove_follower(self, user):
        try:
            self.followers.remove(user)
            user.following.remove(self)
            self.save()
            user.save()
            Signal.send_robust(
                self.__class__, instance=self, user=user, action="remove_follower"
            )
            return True
        except:
            return False

    def block(self, user):
        try:
            self.blocked_users.add(user)
            self.save()
            Signal.send_robust(self.__class__, instance=self, user=user, action="block")
            return True
        except:
            return False
