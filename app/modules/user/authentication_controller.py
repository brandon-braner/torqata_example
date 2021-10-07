from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.user.schemas.user_schemas import AuthSchema, RegistrationSchema, LoginSchema
from app.providers.providers import auth_provider
from app.response_schemas import ErrorResponseSchema

router = APIRouter()


@router.post(
    "/signup",
    response_model=RegistrationSchema,
    status_code=201,
    responses={200: {'model': ErrorResponseSchema}},
    include_in_schema=False
)
async def register(request_body: OAuth2PasswordRequestForm = Depends()):
    auth_response: RegistrationSchema = auth_provider.register(request_body.username, request_body.password)
    if auth_response.error:
        return JSONResponse(
            status_code=200,
            content={
                "data": auth_response.message,
                "error": True
            }
        )

    return auth_response


@router.post(
    "/login",
    response_model=RegistrationSchema,
    status_code=200,
    responses={401: {'model': ErrorResponseSchema}},
)
async def login(request_body: OAuth2PasswordRequestForm = Depends()):
    auth_response: LoginSchema = auth_provider.login(request_body.username, request_body.password)

    if auth_response.error:
        return JSONResponse(
            status_code=401,
            content={
                "data": auth_response.message,
                "error": True
            }
        )

    return auth_response
