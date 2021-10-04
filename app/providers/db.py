from sqlmodel import create_engine, Session

from app.config import settings


def postgres_engine():
    user = settings.postgres_user
    password = settings.postgres_password
    host = settings.postgres_host
    port = settings.postgres_port
    db_name = settings.postgres_db_name

    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

    return create_engine(connection_string)


engine = postgres_engine()


def get_session():
    """Generate a new session from the engine."""
    return Session(engine)
