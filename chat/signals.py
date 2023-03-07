from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.apps import apps
from channels.layers import get_channel_layer
from . import models as chat_models
from . import serializers as chat_serializers
from asgiref.sync import async_to_sync


@async_to_sync
async def send_message_worker(body, from_user, to_user):
    channel_layer = get_channel_layer()

    groups = [f"{from_user}", f"{to_user}"]

    for group in groups:
        await channel_layer.group_send(
            group,
            {
                "type": "receive_message",
                "event": {
                    "handler": "message",
                    "body": body,
                },
            },
        )


@receiver(post_save, sender=chat_models.Message)
def send_message(sender, instance, created, **kwargs):
    print("send_message")
    # if created:
    channel_layer = get_channel_layer()

    body = chat_serializers.MessageSerializer(instance).data

    from_user = instance.from_user.pk
    to_user = instance.to_user.pk
    print(f"|{from_user},{to_user}|")

    send_message_worker(body, from_user, to_user)
