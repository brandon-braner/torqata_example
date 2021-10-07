from typing import Any

from pydantic import BaseModel, Field


class BaseResponseSchema(BaseModel):
    error: bool = Field(default=False, description="Boolean if there was an error or not in the request.")


class ErrorResponseSchema(BaseResponseSchema):
    error: bool = True


class MetaData(BaseModel):
    next_url: str


class APIResponseSchema(BaseResponseSchema):
    meta_data: MetaData
    data: Any
