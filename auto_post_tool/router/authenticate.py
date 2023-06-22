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
            login_token = LoginToken.objects.get(token=token)
        except LoginToken.DoesNotExist:
            raise NotFound(message_code="LOGIN_TOKEN_NOT_FOUND")

        if not login_token.active:
            raise AuthenticationFailed(message_code="INVALID_LOGIN_TOKEN")
        try:
            access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError as exc:
            raise AuthenticationFailed(message_code="INVALID_LOGIN_TOKEN")

        user_uid = access_token.get("user_uid")
        exp_time = access_token.get("exp")

        if user_uid is None or exp_time is None:
            raise ParseError(message_code="INVALID_LOGIN_TOKEN")

        if datetime.fromtimestamp(exp_time) < datetime.now():
            raise AuthenticationFailed(message_code="INVALID_LOGIN_TOKEN")

        try:
            request.user = User.objects.get(uid=user_uid)
            return token
        except User.DoesNotExist as exc:
            raise NotFound("User not found") from exc
