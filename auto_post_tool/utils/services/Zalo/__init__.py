class ZaloService(object):
    def __init__(self, app_id: str, app_secret: str, request_content_type: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.request_content_type = request_content_type

    def generate_access_oath_link(self, oath_code: str):
        return f"app_id={self.app_id}&grant_type=authorization_code&code={oath_code}"

    def generate_access_fefresh_link(self, refresh_token: str):
        return f"app_id={self.app_id}&grant_type=refresh_token&code={refresh_token}"
