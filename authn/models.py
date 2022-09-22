from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser as _User

# Create your models here.


class User(_User):

    bio = models.TextField(blank=True, default="Add Bio", null=True)
    dp = models.ImageField(
        upload_to="dp/", blank=True, default="../static/authn/dp.png"
    )
    cover = models.ImageField(
        upload_to="covers/", blank=True, default="../static/authn/cover.png"
    )
