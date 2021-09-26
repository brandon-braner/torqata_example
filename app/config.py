import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

base_path = pathlib.Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    app_name: str = "Released API"
    app_domain: str = os.environ.get('APP_DOMAIN')
    app_env: str = os.environ.get("APP_ENV")
    app_authorization_cookie: str = 'session'
    cookie_secure: bool = False
    supabase_url: str = os.environ.get('SUPABASE_URL')
    supabase_key: str = os.environ.get('SUPABASE_KEY')
    app_subdomain: str = os.environ.get('APP_SUBDOMAIN')
    cognito_region: str = os.environ.get('COGNITO_REGION')
    cognito_pool_id: str = os.environ.get('COGNITO_POOL_ID')
    cognito_app_client_id: str = os.environ.get('COGNITO_APP_CLIENT_ID')
    cognito_pool_secret_key: str = os.environ.get('COGNITO_POOL_SECRET_KEY')
    jwt_secret_key: str = os.environ.get('JWT_SECRET_KEY')


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
