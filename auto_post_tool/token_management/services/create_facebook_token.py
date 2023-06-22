from datetime import timedelta
from passlib.hash import pbkdf2_sha256
from django.conf import settings
from token_management.models.token import FacebookToken

import requests
class FacebookTokenService:
    """Get the value of access token from FE then turn it into a ThirdPartyToken Object in the DB"""

    @staticmethod
    def create_token(exp, user_id, token=str):
        """function to create a facebook token"""
        enc_token = pbkdf2_sha256.hash(token)
        fb_token = FacebookToken(long_live_token=enc_token, user_id=user_id)
        fb_token.expire_at = fb_token.created_at + timedelta(seconds=exp)
        fb_token.save()

    @staticmethod
    def get_long_lived_access_token(user_id, short_lived_access_token):
        """Generate long-live access token from short-live"""
        try:
            response = requests.post(
                f"""https://graph.facebook.com/oauth/access_token?
                                grant_type=fb_exchange_token&
                                client_id={settings.FACEBOOK_API_APP_ID}&
                                client_secret={settings.FACEBOOK_API_APP_SECRET}&
                                fb_exchange_token={short_lived_access_token}""",
                headers={"Authorization": f"Bearer {short_lived_access_token}"},
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                FacebookTokenService.create_token(response.json().get("expires in"), user_id, response.json().get("access_token"))
            else:
                return response.json().get("error", {}).get("message")
        except TimeoutError as exc:
            raise TimeoutError("Request timed out") from exc

    