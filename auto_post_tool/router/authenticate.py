from django.conf import settings

from ninja.security import HttpBearer

import jwt
from user_account.models.user import User
from utils.exceptions import *
from token_management.models.token import LoginToken
from datetime import datetime, timedelta


# Authenticate token
# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         if token:
#             token = LoginToken.objects.get(token=token)
#             if token.active:
#                 try:
#                     access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#                     user_uid = access_token.get("user_uid")
#                     if user_uid == None:
#                         raise ParseError("Invalid Login Token")

#                     # Retrieve the user from the user_id
#                     request.user = User.objects.get(uid=user_uid)
#                     return token
#                 except jwt.exceptions.DecodeError:
#                     raise AuthenticationFailed("Invalid Login token")
#                 except User.DoesNotExist:
#                     raise NotFound("User not found")
#             else:
#                 raise AuthenticationFailed("Invalid Login token")
#         else:
#             raise ParseError("Token not found")


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token:
            try:
                login_token = LoginToken.objects.get(token=token)
            except LoginToken.DoesNotExist:
                raise NotFound("Login Token not found")
            if login_token.active:
                try:
                    access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
                    print(access_token)
                    user_uid = access_token.get("user_uid")
                    exp_time = access_token.get("exp")
                    if user_uid == None or exp_time == None:
                        raise ParseError("Invalid Login Token")
                    if datetime.fromtimestamp(exp_time) < datetime.now():
                        raise AuthenticationFailed("Login token has expired")
                    request.user = User.objects.get(uid=user_uid)
                    return token
                except jwt.exceptions.DecodeError:
                    raise AuthenticationFailed("Invalid Login token")
                except User.DoesNotExist:
                    raise NotFound("User not found")
            else:
                raise AuthenticationFailed("Invalid Login token")
        else:
            raise ParseError("Token not found")
