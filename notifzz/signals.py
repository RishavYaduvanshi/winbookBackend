from django.dispatch import receiver
from . import models
from authn import signals as authn_signals, models as authn_models
from postapp import signals as postapp_signals, models as postapp_models
from . import services


@receiver(authn_signals.follow_signal)
def follow_handler(sender, instance, user, action, **kwargs):
    

    if action == "follow":
        notif = models.Notification.objects.create(
            title="New Follower",
            description="{actor} started following you".format(actor=instance),
            users=[user],
            actor=instance,
        )
        
        services.send_notification(notif)


@receiver(postapp_signals.post_signal)
def like_handler(sender, instance, user, action, **kwargs):
    

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
        services.send_notification(notif)

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
        services.send_notification(notif)


@receiver(postapp_signals.comment_signal)
def comment_handler(sender, instance, user, action, **kwargs):
    

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
        services.send_notification(notif)

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
        services.send_notification(notif)
