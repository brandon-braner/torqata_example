from app.modules.user.providers.authentication.aws_auth_provider import AwsAuthenticationProvider
from app.providers.db import postgres_db

# Auth Provider
auth_provider = AwsAuthenticationProvider()

# Database Providers
postgres_provider = postgres_db()
