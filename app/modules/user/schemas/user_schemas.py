from typing import Optional, Dict

from pydantic import BaseModel, Field, EmailStr

from app.response_schemas import BaseResponseSchema


class AuthSchema(BaseModel):
    username: str = Field(description="Username that your user wishes to use for your auth provider")
    password: str = Field(description="Non hashed password that your user wishes to use for your auth provider")


class UserSchema(BaseModel):
    username: str = Field(description="Username provided by the auth platform")
    email: Optional[EmailStr] = Field(description="Users email address, this may also be the username")
    meta: Optional[Dict] = Field(default={},
                                 description="Metadata for the user, this could include things like address, phone")
    id: Optional[str] = Field(description="Users id from the auth platform")


class RegistrationSchema(BaseResponseSchema):
    access_token: str = Field(description="Access token for oauth providers or api tokens.")
    refresh_token: Optional[str] = Field(description="Refresh token for oauth providers")
    user: UserSchema = Field(description="User data returned from auth provider.")
    message: Optional[str] = Field(description="message to return along with api call.")


class LoginSchema(RegistrationSchema):
    pass
