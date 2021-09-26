from app.modules.user.providers.authentication.auth_provider_interface import IAuthProvider
from app.modules.user.schemas.user_schemas import UserSchema, RegistrationSchema
from app.providers.db import get_session
from app.modules.user.models.user import User, generate_api_key
from app.security import hash_password, verify_password


class SQLModelAuthProvider(IAuthProvider):

    def __init__(self):
        self.session = get_session()

    def register(self, username: str, password: str):
        hashed_password = hash_password(password)
        api_key = generate_api_key()
        user = User(
            username=username,
            password=hashed_password,
            api_key=api_key
        )
        self.session.add(user)
        self.session.commit()

        user_schema = UserSchema(
            username=username,
            email=username
        )

        registration_schema = RegistrationSchema(
            access_token = api_key,
            user=user_schema,
            error=False
        )

        return registration_schema

    def login(self, username: str, password: str):
        pass

    def logout(self):
        pass
