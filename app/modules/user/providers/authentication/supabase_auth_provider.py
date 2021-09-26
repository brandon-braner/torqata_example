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
            if user['status_code'] == 200:
                registration_schema = RegistrationSchema(
                    access_token=user['access_token'],
                    refresh_token=user['refresh_token'],
                    error=False
                )
            else:
                registration_schema = RegistrationSchema(
                    message="Encountered an error while registering, please try again.",
                    error=True
                )

            return registration_schema
        except Exception:
            pass

    def login(self, username: str, password: str) -> LoginSchema:
        try:
            user = self.client.auth.sign_in(email=username, password=password)

            if user['status_code'] == 200:
                user_details = user['user']
                login_schema = LoginSchema(
                    access_token=user['access_token'],
                    refresh_token=user['refresh_token'],
                    error=False,
                    user={
                        'email': user_details['email'],
                        'role': user_details['role'],
                        'id': user_details['id']
                    }
                )
            else:
                login_schema = LoginSchema(
                    error=True,
                    message='Something went wrong, please try again.'
                )

            return login_schema

        except Exception:
            pass

    def logout(self):
        pass

    def user_details(self, access_token: str):
        user = self.client.auth.api.get_user(access_token)
        if user['status_code'] == 200:
            user_schema = UserSchema(
                email=user['email'],
                username=user['email'],
                id=user['id']
            )

            return user_schema

        else:
            login_schema = LoginSchema(
                error=True,
                message='Something went wrong, please try again.'
            )
            return login_schema
