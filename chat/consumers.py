from custom import consumer
from typing import Dict


class ChatConsumer(consumer.Consumer):
    async def echo(self, content, **kwargs) -> Dict:
        return content

    ROUTING = {
        "echo": echo,
    }
