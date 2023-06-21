from datetime import datetime, timedelta
from django.conf import settings
import jwt

from token_management.models.token import LoginToken


class CreateLoginTokenService:
    """Get the value of JWT token then turn it into a LoginToken Object in the DB"""

    def create_token(self, uid=str):
        """function to create a jwt token for logging in"""             
        access_token = jwt.encode(
            {"user_uid": uid, "exp": datetime.now() + timedelta(hours=int(settings.JWT_EXPIRED_TIME))},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        jwt_token = LoginToken(token=access_token)
        jwt_token.save()
        return access_token
