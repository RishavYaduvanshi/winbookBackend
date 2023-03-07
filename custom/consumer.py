from channels.generic import websocket
from typing import Dict, Any, Callable


class Consumer(websocket.AsyncJsonWebsocketConsumer):

    ROUTING: Dict[str, Callable]

    AUTH = False

    async def connect(self):
        await super().connect()

        user = self.scope["user"] if self.scope["user"].is_authenticated else None

        if self.AUTH and user is None:
            await self.send_json({"message": "unauthorized"})
            return await self.close()

        return await self.send_json(
            {
                "message": "connected",
                "user": str(user),
            }
        )

    async def handle(self, content: Dict[str, Any], **kwargs) -> Dict:
        """
        Handle incoming messages and route them to the appropriate handler.
        """
        return await self.ROUTING.get(content.get("handler", ""), Consumer.no_route)(
            self, content, **kwargs
        )

    async def no_route(self, content, **kwargs) -> Dict:
        return {"message": f"No route for {content.get('handler', '')}"}

    async def receive_json(self, content, **kwargs) -> None:
        return await self.send_json(await self.handle(content, **kwargs), **kwargs)
