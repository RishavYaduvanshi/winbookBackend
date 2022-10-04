# Generated by Django 4.1 on 2022-10-04 08:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notifzz", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="user",
        ),
        migrations.AddField(
            model_name="notification",
            name="users",
            field=models.ManyToManyField(
                related_name="notifications", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
