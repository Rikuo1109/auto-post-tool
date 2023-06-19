from django.conf import settings

from ninja.security import HttpBearer

import jwt
from user_account.models.user import User
from utils.exceptions import *


class BlacklistToken:
    token_list = []

    @classmethod
    def add_token(cls, token):
        cls.token_list.append(token)

    @classmethod
    def check_token(cls, token):
        return token in cls.token_list

    @classmethod
    def print(self):
        print(self.token_list)


# Authenticate token
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token:
            if BlacklistToken.check_token(token):
                raise NotAuthenticated
            try:
                access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_email = access_token["user_email"]

                # Retrieve the user from the user_id
                request.user = User.objects.get(email=user_email)
                return token
            except jwt.exceptions.DecodeError:
                return {"detail": "Invalid access token."}
            except User.DoesNotExist:
                return {"detail": "User does not exist."}
