import requests
from django.conf import settings
from utils.exceptions.exceptions import NotFound


def get_user_fb_id(token: str):
    response = requests.get(settings.FACEBOOK_GET_USERID_URL, params={"access_token": token})
    try:
        response_data = response.json().get("id")
    except requests.JSONDecodeError:
        raise NotFound(message_code="FACEBOOK_ID_NOT_FOUND")
    return response_data


def get_user_fb_page_info(token: str):
    user_id = get_user_fb_id(token)
    response = requests.get(
        f"https://graph.facebook.com/{user_id}", params={"fields": "accounts", "access_token": token}
    )
    print(response.json())
    try:
        page_data = response.json().get("accounts").get("data")
        page_info = [
            {"name": page.get("name"), "page_id": page.get("id"), "page_access_token": page.get("access_token")}
            for page in page_data
        ]
        return page_info
    except AttributeError:
        raise NotFound(message_code="FACEBOOK_PAGE_NOT_FOUND")
