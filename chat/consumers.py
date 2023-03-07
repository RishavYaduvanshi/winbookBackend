from custom import consumer
from typing import Dict


class ChatConsumer(consumer.Consumer):
    AUTH = True

    async def echo(self, content, **kwargs) -> Dict:
        return content

    async def connect(self):
        user = await super().connect()
        if user is None:
            return None
        await self.channel_layer.group_add(f"{user.pk}", self.channel_name)
        await self.send_json({"group": f"{user.pk}", "channel": self.channel_name})

    ROUTING = {
        "echo": echo,
    }

    async def receive_message(self, event):
        await self.send_json(event.get("event"))
