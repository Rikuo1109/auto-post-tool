from datetime import timedelta

from passlib.hash import pbkdf2_sha256
from token_management.models.token import ZaloToken


class ZaloTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp, user_id, access_token: str, refresh_token: str):
        """function to create a facebook token"""
        encrypted_access_token = pbkdf2_sha256.hash(access_token)
        encrypted_refresh_token = pbkdf2_sha256.hash(refresh_token)
        zalo_token = ZaloToken(access_token=encrypted_access_token, refresh_token=encrypted_refresh_token, user_id=user_id)
        zalo_token.expire_at = zalo_token.created_at + timedelta(seconds=exp)
        zalo_token.save()
