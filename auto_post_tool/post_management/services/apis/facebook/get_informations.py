import requests

from . import USER_HEADERS, FACEBOOK_API_VERSION, USER_ID


class GetInformationServices:
    def __init__(self):
        pass

    def get_user_info(self):
        response = requests.get(f"""https://graph.facebook.com/{FACEBOOK_API_VERSION}/{"me"}""", headers=USER_HEADERS)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            error_message = response.json().get("error", {}).get("message")
            return error_message

    def get_user_pages(self):
        response = requests.get(
            f"""https://graph.facebook.com/{USER_ID}/accounts?fields=name,access_token""", headers=USER_HEADERS
        )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            error_message = response.json().get("error", {}).get("message")
            return error_message
