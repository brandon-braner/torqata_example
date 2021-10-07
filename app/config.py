import enum
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
    api_domain: str = os.environ.get('API_DOMAIN')
    app_env: str = os.environ.get("APP_ENV")
    app_authorization_cookie: str = 'session'
    cookie_secure: bool = False

    # postgres
    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_host: str = os.environ.get("POSTGRES_HOST")
    postgres_port: int = os.environ.get("POSTGRES_PORT")
    postgres_db_name: str = os.environ.get("POSTGRES_DB_NAME")

    # cloud sql
    socket_path = "/cloudsql"
    cloud_sql_instance_name = 'torqataexample:us-central1:torqataexample'

    neo4j_protocol: str = os.environ.get("NEO4J_PROTOCOL")
    neo4j_host: str = os.environ.get("NEO4J_HOST")
    neo4j_port: str = os.environ.get("NEO4J_PORT")
    neo4j_user: str = os.environ.get("NEO4J_USER")
    neo4j_password: str = os.environ.get("NEO4J_PASSWORD")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


class AppEnvironments(enum.Enum):
    prod = 'PROD'
    local = 'LOCAL'
