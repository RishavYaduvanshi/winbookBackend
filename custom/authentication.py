from channels import auth
from channels.db import database_sync_to_async


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
        query = self.User.objects.filter(auth_token__pk=token)
        return query.first() if query.exists() else None

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

            from django.contrib.auth.models import AnonymousUser

            scope["user"] = scope["user"] or AnonymousUser()

        return await super().__call__(scope, receive, send)
