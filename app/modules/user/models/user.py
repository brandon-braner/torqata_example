import secrets
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model related to the user table in the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    api_key: str


def generate_api_key():
    return secrets.token_hex(32)
