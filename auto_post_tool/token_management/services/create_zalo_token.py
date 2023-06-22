from datetime import timedelta

from passlib.hash import pbkdf2_sha256
from token_management.models.token import ZaloToken


class FacebookTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp, user_id, a_token: str, r_token: str):
        """function to create a facebook token"""
        enc_access_token = pbkdf2_sha256.hash(a_token)
        enc_refresh_token = pbkdf2_sha256.hash(r_token)
        zl_token = ZaloToken(access_token=enc_access_token, refresh_token=enc_refresh_token, user_id=user_id)
        zl_token.expire_at = zl_token.created_at + timedelta(seconds=exp)
        zl_token.save()
