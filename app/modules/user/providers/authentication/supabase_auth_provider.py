from supabase_py import Client

from app.modules.user.providers.authentication.auth_provider_interface import IAuthProvider
from app.schemas.response_schemas import RegistrationSchema, LoginSchema
from app.modules.user.schemas.user_schemas import UserSchema


class SupabaseAuthProvider(IAuthProvider):
    """
    Authentication provider for Supabase using email and password authentication.
    To use this provider open app/providers/providers.py import this file and
    switch the auth_provider to SupabaseAuthProvider().
    """
    def __init__(self, client: Client):
        self.client: Client = client

    def register(self, username: str, password: str) -> RegistrationSchema:
        try:
            user = self.client.auth.sign_up(email=username, password=password)
            return RegistrationSchema(
                    access_token=user['access_token'],
                    refresh_token=user['refresh_token'],
                    error=False
                ) if user['status_code'] == 200 else RegistrationSchema(
                    message="Encountered an error while registering, please try again.",
                    error=True
                )
        except Exception:
            pass

    def login(self, username: str, password: str) -> LoginSchema:
        try:
            user = self.client.auth.sign_in(email=username, password=password)

            if user['status_code'] != 200:
                return LoginSchema(
                    error=True,
                    message='Something went wrong, please try again.'
                )

            user_details = user['user']
            return LoginSchema(
                    access_token=user['access_token'],
                    refresh_token=user['refresh_token'],
                    error=False,
                    user={
                        'email': user_details['email'],
                        'role': user_details['role'],
                        'id': user_details['id']
                    }
                )
        except Exception:
            pass

    def logout(self):
        pass

    def user_details(self, access_token: str):
        user = self.client.auth.api.get_user(access_token)
        if user['status_code'] == 200:
            return UserSchema(
                email=user['email'],
                username=user['email'],
                id=user['id']
            )

        else:
            return LoginSchema(
                error=True,
                message='Something went wrong, please try again.'
            )
