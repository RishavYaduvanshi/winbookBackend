from django.db import models


class Post(models.Model):
    url = models.URLField(  )
    caption = models.CharField(max_length=200)
    liked_by = models.ManyToManyField('authn.User', related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



