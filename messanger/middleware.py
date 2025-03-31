from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'sec-websocket-protocol' in headers:
            try:
                token_name, token_key = headers[b'sec-websocket-protocol'].decode().split(', ')
                if token_name == 'Token':
                    scope['user'] = await self.get_user(token_key)
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            return Token.objects.get(key=token_key).user
        except Token.DoesNotExist:
            return AnonymousUser()