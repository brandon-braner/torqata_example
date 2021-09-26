from typing import List, Dict

import boto3
import requests
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, jwk
from jose.utils import base64url_decode
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN

from app.config import get_settings
from app.modules.user.providers.authentication.auth_provider_interface import IAuthProvider
from app.modules.user.schemas.user_schemas import UserSchema, RegistrationSchema
from app.response_schemas import ErrorResponseSchema

JWK = Dict[str, str]


class JWKS(BaseModel):
    keys: List[JWK]


class AwsAuthenticationProvider(IAuthProvider):
    """
    Authentication provider for AWS Cognition using email and password authentication.
    To use this provider open app/providers/providers.py import this file and
    switch the auth_provider to AwsAuthenticationProvider().
    """

    def __init__(self):
        settings = get_settings()
        self.client = boto3.client('cognito-idp')
        self.client_id = settings.cognito_app_client_id
        self.pool_id = settings.cognito_pool_id
        self.client_secret = settings.cognito_pool_secret_key
        self.cognito_region = settings.cognito_region
        # Attributes we are looking to get back from AWS
        self.user_attributes = ['name', 'email']

    def get_jwks(self):
        """Get jwks from aws."""
        jwks = JWKS.parse_obj(
            requests.get(
                f"https://cognito-idp.{self.cognito_region}.amazonaws.com/"
                f"{self.pool_id}/.well-known/jwks.json"
            ).json()
        )

        return jwks

    def register(self, username: str, password: str) -> RegistrationSchema:
        """Method to register a new user."""
        resp = self.client.sign_up(
            ClientId=self.client_id,
            Username=username,
            Password=password
        )

        # log user in
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            auth_response = self.client.admin_initiate_auth(
                AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                ClientId=self.client_id,
                UserPoolId=self.pool_id
            )

            authentication_result = auth_response['AuthenticationResult']

            # get user from aws
            user = self._get_user_from_aws(authentication_result['AccessToken'])
            user_schema = UserSchema(
                username=user.get('email', ''),
                email=user.get('email', '')
            )

            registration_schema = RegistrationSchema(
                access_token=authentication_result['AccessToken'],
                refresh_token=authentication_result['RefreshToken'],
                user=user_schema,
                error=False
            )
        else:
            registration_schema = RegistrationSchema(
                message="Encountered an error while registering, please try again.",
                error=True
            )

        return registration_schema

    def login(self, username: str, password: str) -> RegistrationSchema:
        """
        Method to login from the app, not to be used with the api.
        Implemented using server side auth flow from cognito docs.
        https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html#amazon-cognito-user-pools-server-side-authentication-flow
        """
        try:
            resp = self.client.admin_initiate_auth(
                AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                ClientId=self.client_id,
                UserPoolId=self.pool_id
            )
            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:

                authentication_result = resp['AuthenticationResult']

                user_details = self._get_user_from_aws(authentication_result['AccessToken'])
                user_schema = UserSchema(
                    username=user_details.get('email', ''),
                    email=user_details.get('email', ''),
                    id=user_details.get('id', '')
                )
                login_schema = RegistrationSchema(
                    access_token=authentication_result['AccessToken'],
                    refresh_token=authentication_result['RefreshToken'],
                    error=False,
                    user=user_schema
                )
            else:
                login_schema = RegistrationSchema(
                    error=True,
                    message='Something went wrong, please try again.'
                )
            return login_schema
        except:
            # TODO handle exception
            pass

    def get_user(self, access_token: str):
        try:
            user = self._get_user_from_aws(access_token)
            return user
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid Request")

    def api_authentication(self, user_data: OAuth2PasswordRequestForm = Depends()):
        """Method to get authentication information for public api."""
        try:
            response = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': user_data.username,
                    'PASSWORD': user_data.password
                },
                ClientId=self.client_id
            )
            authentication_result = response['AuthenticationResult']
            access_token = authentication_result['AccessToken']
            decoded_access_token = self.decode_access_token(access_token)
            data = {
                'access_token': authentication_result['AccessToken'],
                'refresh_token': authentication_result['RefreshToken'],
                'expire_timestamp': decoded_access_token['exp'],
                'token_type': authentication_result['TokenType']
            }
            return {'data': data, 'error': False}
        except Exception as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="JWK invalid")

            data = 'Username or password are incorrect. Please try again.'
            return {'data': data, 'error': True}

    def logout(self):
        pass

    # def update_user_attributes(self, access_token: str, attributes: UserDetails):
    #     self.client.update_user_attributes(
    #         UserAttributes=[
    #             attributes.dict()
    #         ],
    #         AccessToken=access_token
    #     )
    #
    def _get_user_from_aws(self, access_token):
        decoded_jwt_token = self.decode_access_token(access_token, False)
        try:
            user = self.client.admin_get_user(
                UserPoolId=self.pool_id,
                Username=decoded_jwt_token['username']
            )
        except Exception as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Username or password invalid.")
        response = dict()
        # Take user attributes and map them to return to application
        for attribute in user['UserAttributes']:
            if attribute['Name'] in self.user_attributes:
                key = attribute['Name'].lower()
                response[key] = attribute['Value']
            response['id'] = user['Username']
        return response

    def verify_access_token(self, access_token: str):
        """Verify jwt we got from aws."""
        verified = False
        public_key = ''
        jwks = self.get_jwks()
        jwt_headers = jwt.get_unverified_header(access_token)
        key_id = jwt_headers['kid']
        for _jwk in jwks.keys:
            if key_id == _jwk['kid']:
                verified = True
                public_key = jwk.construct(_jwk)
                break
        if not verified:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")

        message, encoded_signature = str(access_token).rsplit('.', 1)
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")

    def decode_access_token(self, access_token, verify=True):
        """Decode access token we got from aws."""
        if verify:
            self.verify_access_token(access_token)
        # we can return unverified claims since we just verified the token
        return jwt.get_unverified_claims(access_token)
    #
    # def generate_cookie(self, response: Response, jwt: UserJwt):
    #     settings = get_settings()
    #     jwt_decoded = self.decode_access_token(jwt.access_token, False)
    #     response.set_cookie(key=settings.cookie_name, value=jwt.access_token, domain=settings.app_domain, httponly=True,
    #                         secure=settings.cookie_secure, expires=jwt_decoded['exp'])
