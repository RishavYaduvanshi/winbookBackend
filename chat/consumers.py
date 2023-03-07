from custom import consumer
from typing import Dict
from rest_framework.serializers import ModelSerializer
from . import models
from custom import utils


class ChatConsumer(consumer.Consumer):

    AUTH = True

    async def echo(self, content, **kwargs) -> Dict:
        return content

    async def connect(self):
        user = await super().connect()
        if user is None:
            return None
        await self.channel_layer.group_add(f"{user.pk}", self.channel_name)

    async def receive_message(self, event):
        await self.send_json(event.get("event"))

    async def message(self, content, **kwargs):
        class MessageSerializer(ModelSerializer):
            class Meta:
                model = models.Message
                fields = ["from_user", "to_user", "message"]

        body = content.get("body")
        body["from_user"] = self.scope["user"].pk
        serializer = MessageSerializer(data=body)
        await utils.saveSerializer(serializer)

    ROUTING = {
        "echo": echo,
        "message": message,
    }
