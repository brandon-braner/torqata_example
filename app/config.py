import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

base_path = pathlib.Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    app_name: str = "Torgata API"
    app_domain: str = os.environ.get('APP_DOMAIN')
    app_env: str = os.environ.get("APP_ENV")
    app_authorization_cookie: str = 'session'
    cookie_secure: bool = False

    # postgres
    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_host: str = os.environ.get("POSTGRES_HOST")
    postgres_port: int = os.environ.get("POSTGRES_PORT")
    postgres_db_name: str = os.environ.get("POSTGRES_DB_NAME")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
