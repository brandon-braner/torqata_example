from typing import Optional

from pydantic import BaseModel, Field


class BaseResponseSchema(BaseModel):
    message: Optional[str] = Field(description='Optional message to return with response. Example describe the error.')
    error: bool = Field(default=False, description="Boolean if there was an error or not in the request.")


class ErrorResponseSchema(BaseResponseSchema):
    error: bool = True


# class UserJwt(BaseModel):
#     access_token: str
#     username: str = ''
#     email: str = ''
#     name: str = ''
