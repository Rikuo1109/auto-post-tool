import requests

from . import USER_HEADERS, USER_ACCESS_TOKEN, FACEBOOK_API_APP_ID, FACEBOOK_API_APP_SECRET


class GetAccessTokenServices:
    def __init__(self):
        pass

    def get_long_lived_access_token(self):
        requests.post(
            f"""https://graph.facebook.com/oauth/access_token?
                            grant_type=fb_exchange_token&
                            client_id={FACEBOOK_API_APP_ID}&
                            client_secret={FACEBOOK_API_APP_SECRET}&
                            fb_exchange_token={USER_ACCESS_TOKEN}""",
            headers=USER_HEADERS,
        )
