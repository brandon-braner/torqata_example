from typing import Union

from fastapi import HTTPException
from sqlmodel import select
from starlette.status import HTTP_401_UNAUTHORIZED

from app.modules.user.models.user import User, generate_api_key
from app.modules.user.providers.authentication.auth_provider_interface import IAuthProvider
from app.modules.user.schemas.user_schemas import UserSchema, RegistrationSchema, LoginSchema
from app.providers.db import get_session
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
            access_token=api_key,
            user=user_schema,
            error=False
        )

        return registration_schema

    def login(self, username: str, password: str) -> LoginSchema:
        user = self.get_user(username)

        if not user:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        password_is_valid = verify_password(password, user.password)

        if password_is_valid:
            login_schema = LoginSchema(
                access_token=user.api_key,
                user=user
            )
            login_schema.user.email = user.username
            return login_schema

    def logout(self):
        pass

    def get_user(self, access_token: str) -> Union[User, None]:
        with get_session() as session:
            stmt = select(User).where(User.api_key == access_token)
            result = session.exec(stmt)
            user = result.one_or_none()
            return user.dict()