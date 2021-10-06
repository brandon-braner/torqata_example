import secrets
from typing import Optional, Union

from sqlmodel import Field, SQLModel, select

from app.providers.db import get_session


class User(SQLModel, table=True):
    """User model related to the user table in the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    api_key: str


def generate_api_key():
    return secrets.token_hex(32)


def get_user(username: str) -> Union[User, None]:
    with get_session() as session:
        stmt = select(User).where(User.username == username)
        result = session.exec(stmt)
        return result.one_or_none()
