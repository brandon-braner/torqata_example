from neo4j import GraphDatabase
from py2neo import Graph
from sqlmodel import create_engine, Session

from app.config import settings, AppEnvironments


def postgres_engine():
    user = settings.postgres_user
    password = settings.postgres_password
    host = settings.postgres_host
    port = settings.postgres_port
    db_name = settings.postgres_db_name
    socket_path = settings.socket_path
    instance = settings.cloud_sql_instance_name

    # connection string for local
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

    if settings.app_env == AppEnvironments.prod:
        connection_string = f"postgresql+psycopg2://{user}:{password}@/{db_name}?host={socket_path}/{instance}"

    return create_engine(connection_string)


engine = postgres_engine()


def get_session():
    """Generate a new session from the engine."""
    return Session(engine)


def neo_engine():
    """Get instance of neo4j driver."""
    protocol = settings.neo4j_protocol
    host = settings.neo4j_host
    port = settings.neo4j_port
    user = settings.neo4j_user
    password = settings.neo4j_password

    connection_string = f"{protocol}://{host}:{port}"
    return GraphDatabase.driver(connection_string, auth=(user, password))


def neo_graph() -> Graph:
    """Get instance of py2neo"""
    protocol = settings.neo4j_protocol
    host = settings.neo4j_host
    port = settings.neo4j_port
    user = settings.neo4j_user
    password = settings.neo4j_password

    connection_string = f"{protocol}://{host}:{port}"
    return Graph(connection_string, user=user, password=password)
