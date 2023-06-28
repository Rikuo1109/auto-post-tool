import requests


def get_user_id(token: str):
    response = requests.get(f"https://graph.facebook.com/v17.0/me?access_token={token}")
    return response.json().get("id")


def get_user_page_info(token: str, user_id: str):
    response = requests.get(f"https://graph.facebook.com/{user_id}?fields=accounts&access_token={token}")
    page_data = response.json().get("accounts").get("data")
    page_info = [{"name": page["name"], "id": page["id"]} for page in page_data]
    return page_info
