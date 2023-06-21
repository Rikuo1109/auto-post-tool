from datetime import datetime, timedelta
from django.conf import settings
import jwt
from token_management.models.token import ThirdPartyToken


class Create3rdTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    def __init__(self) -> None:
        pass

    def create_token(self, uid=str) {
        access_token_payload = {
            "user_uid": uid,
            "exp": datetime.now() + timedelta(hour)
        }
    }
