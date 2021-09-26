from fastapi import Response

from app.config import settings


def generate_and_set_cookie(response: Response, key: str, value: str):
    response.set_cookie(key=key,
                        value=value,
                        domain=settings.app_domain,
                        httponly=True,
                        secure=settings.cookie_secure
                        )
