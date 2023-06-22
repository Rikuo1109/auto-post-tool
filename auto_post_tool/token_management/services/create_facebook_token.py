from datetime import timedelta
from passlib.hash import pbkdf2_sha256
from token_management.models.token import FacebookToken

class FacebookTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp, token=str):
        """function to create a facebook token"""
        enc_token = pbkdf2_sha256.hash(token)
        fb_token = FacebookToken(long_live_token=enc_token)
        fb_token.expire_at = fb_token.created_at + timedelta(seconds=exp)
        fb_token.save()
    