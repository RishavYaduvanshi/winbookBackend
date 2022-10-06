from django.dispatch import receiver
from . import models
from authn import signals as authn_signals, models as authn_models
from postapp import signals as postapp_signals, models as postapp_models


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
