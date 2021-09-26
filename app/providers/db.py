from sqlmodel import SQLModel, create_engine
from app.config import settings


def postgres_db():
    user = settings.postgres_user
    password = settings.postgres_password
    host = settings.postgres_host
    port = settings.postgres_port
    db_name = settings.postgres_db_name

    connection_string = f"postgresql+asyncpg://{user}:{password}@{host}{port}/{db_name}"
    return create_engine(connection_string)
