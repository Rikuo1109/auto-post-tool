from datetime import datetime

from django.conf import settings

from ninja.security import HttpBearer

import jwt
from token_management.models.token import LoginToken
from user_account.models.user import User
from utils.exceptions import AuthenticationFailed, NotFound, ParseError


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if not token:
            raise ParseError(message_code="INVALID_LOGIN_TOKEN")
        try:
            # Decode the access token
            access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = access_token["user_id"]
            request.user = User.objects.get(uid=user_id)
            return token
        except jwt.exceptions.DecodeError:
            return {"detail": "Invalid access token."}
        except User.DoesNotExist:
            return {"detail": "User does not exist."}
