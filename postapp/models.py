from unicodedata import name
from django.db import models


class Post(models.Model):
    user = models.ForeignKey('authn.User', on_delete=models.CASCADE)
    url = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=200)
    liked_by = models.ManyToManyField('authn.User', related_name='likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



