from fastapi import Request
from starlette.authentication import (
    AuthenticationBackend, SimpleUser, AuthCredentials, AuthenticationError
)

from app.config import settings
from app.providers.providers import auth_provider

NON_AUTH_ENDPOINTS = [
    '/login',
    '/signup',
    '/docs',
    '/redoc',
    '/openapi.json'
]


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        needs_authorization = await self.request_needs_authorization(request)
        if not needs_authorization:
            return

        authorization_header = await self.get_authorization_header(request)
        authorization_cookie = await self.get_authorization_cookie(request)

        # return a 401 if they are not authenticated
        if not authorization_header and not authorization_cookie:
            raise AuthenticationError('Unable to authenticate user.')

        access_token = authorization_header if len(authorization_header) > 0 else authorization_cookie

        user = auth_provider.get_user(access_token)
        if not user:
            # refresh with access token from database(maybe redis)
            raise AuthenticationError('Unable to authenticate user.')

        username = user['email'] if user.get('email', None) else user['username']
        return AuthCredentials(["authenticated"]), SimpleUser(username)

    async def request_needs_authorization(self, request: Request):
        """
        If Path is in NON AUTH ENDPOINTS this will return false so we don't need to authenticate user the endpoint.
        """
        path = request.url.components.path
        return path not in NON_AUTH_ENDPOINTS

    async def get_request_host(self, request: Request):
        return request.headers.get('Host', None)

    async def get_authorization_header(self, request: Request):
        """Get the authorization_header remove bearer and whatever is left should be auth token."""
        header = request.headers.get('Authorization', None)
        if header:
            return header.replace('Bearer', '').strip()
        return None

    async def get_authorization_cookie(self, request: Request):
        """Get the cookie and return it that should be the auth token."""
        cookie_name = settings.app_authorization_cookie
        return request.cookies.get(cookie_name, None)
