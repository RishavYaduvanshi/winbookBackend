from channels import auth
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class TokenAuthenticationMiddleware(auth.BaseMiddleware):
    """
    Token based authentication middleware
    """

    def __init__(self, inner):
        super().__init__(inner)
        self.User = auth.get_user_model()

    def convert_to_str(self, value):
        try:
            return value.decode() if isinstance(value, bytes) else value
        except UnicodeDecodeError:
            return value

    @database_sync_to_async
    def resolve_token(self, token: str):
        return self.User.objects.get(auth_token__pk=token)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            # convert headers to dict from list
            scope["headers"] = {
                self.convert_to_str(k): self.convert_to_str(v)
                for k, v in scope["headers"]
            }

            token = scope.get("headers").get("Authorization", None)

            if token is None:
                token = scope.get("headers").get("authorization", None)

            if token is not None:
                token = token.split(" ")[1]
                scope["user"] = await self.resolve_token(token)
            else:
                scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
