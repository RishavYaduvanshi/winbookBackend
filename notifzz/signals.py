from django.dispatch import receiver
from . import models
from authn import signals as authn_signals, models as authn_models
from postapp import signals as postapp_signals, models as postapp_models
from django.db.models.signals import post_save
from push_notifications.models import GCMDevice
from rest_framework import serializers


@receiver(authn_signals.follow_signal)
def follow_handler(sender, instance, user, action, **kwargs):
    print("instance: ", instance)
    print("user: ", user)
    print("action: ", action)
    print("kwargs: ", kwargs)

    if action == "follow":
        models.Notification.objects.create(
            title="New Follower",
            description="{actor} started following you".format(actor=instance),
            users=[user],
            actor=instance,
        )


@receiver(postapp_signals.post_signal)
def like_handler(sender, instance, user, action, **kwargs):
    print("instance: ", instance)
    print("user: ", user)
    print("action: ", action)
    print("kwargs: ", kwargs)

    if action == postapp_models.Post.POST_LIKED:
        notif = models.Notification(
            title="New Like",
            description="{actor} liked your post".format(actor=user),
            post=instance,
            actor=user,
        )
        notif.save()
        notif.users.add(instance.user)
        notif.save()

    elif action == postapp_models.Post.POST_CREATED:
        if user.followers.count() == 0:
            return
        notif = models.Notification(
            title="New Post",
            description="{actor} created a new post".format(actor=instance.user),
            post=instance,
        )
        notif.save()
        notif.users.set(user.followers.all())
        notif.save()


@receiver(postapp_signals.comment_signal)
def comment_handler(sender, instance, user, action, **kwargs):
    print("instance: ", instance)
    print("user: ", user)
    print("action: ", action)
    print("kwargs: ", kwargs)

    if action == postapp_models.Comment.COMMENT_CREATED:
        if instance.post.user == user:
            return
        notif = models.Notification(
            title="New Comment",
            description="{actor} commented on your post".format(actor=user),
            post=instance.post,
            actor=user,
        )
        notif.save()
        notif.users.add(instance.post.user)
        notif.save()

    elif action == postapp_models.Comment.REPLY_CREATED:
        if instance.replied_to.user == user:
            return
        notif = models.Notification(
            title="New Reply",
            description="{actor} replied to your comment".format(actor=user),
            post=instance.post,
            actor=user,
        )
        notif.save()
        notif.users.add(instance.replied_to.user)
        notif.save()


@receiver(post_save, sender=models.Notification)
def notification_handler(sender, instance, created, **kwargs):
    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Notification
            exclude = ["users"]

    if created:
        d = NotificationSerializer(instance).data
        desc = d.pop("description")
        devices = GCMDevice.objects.filter(user__in=instance.users.all())
        devices.send_message(desc, extra=d)
