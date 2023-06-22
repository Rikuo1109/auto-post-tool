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
            raise ParseError("Token not found")
        try:
            login_token = LoginToken.objects.get(token=token)
        except LoginToken.DoesNotExist as e:
            raise NotFound("Login Token not found") from e

        if not login_token.active:
            raise AuthenticationFailed("Invalid Login token")
        try:
            access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError as exc:
            raise AuthenticationFailed("Invalid Login token") from exc

        user_uid = access_token.get("user_uid")
        exp_time = access_token.get("exp")

        if user_uid is None or exp_time is None:
            raise ParseError("Invalid Login Token")

        if datetime.fromtimestamp(exp_time) < datetime.now():
            raise AuthenticationFailed("Login token has expired")

        try:
            request.user = User.objects.get(uid=user_uid)
            return token
        except User.DoesNotExist as exc:
            raise NotFound("User not found") from exc
