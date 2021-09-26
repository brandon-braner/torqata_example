from app.modules.user.providers.authentication.aws_auth_provider import AwsAuthenticationProvider
from app.modules.user.providers.authentication.sql_model_auth_provider import SQLModelAuthProvider
from app.providers.db import postgres_engine

# Auth Provider
# auth_provider = AwsAuthenticationProvider()
auth_provider = SQLModelAuthProvider()

# Database Providers
postgres_provider = postgres_engine()
