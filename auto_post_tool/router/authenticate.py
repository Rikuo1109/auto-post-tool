from django.conf import settings

from ninja.security import HttpBearer

import jwt
from user_account.models.user import User


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        print(token)
        try:
            # Decode the access token
            access_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = access_token["user_id"]

            # Retrieve the user from the user_id
            request.user = User.objects.get(id=user_id)
            print(request.user.password)
            return token
        except jwt.exceptions.DecodeError:
            return {"detail": "Invalid access token."}
        except User.DoesNotExist:
            return {"detail": "User does not exist."}
