from post_management.services.apis.facebook.base_api import BaseFacebookApiService
from utils.enums.post import PostTypeFormatEnum
from utils.functions.markdown_to_text import markdown_to_text


class GroupsFacebookApiService(BaseFacebookApiService):
    def __init__(self, post_management):
        super().__init__(post_management=post_management, base_id="group_id")

    def prepair_params_feed(self):
        params = super().prepair_params_feed()
        params["formatting"] = PostTypeFormatEnum.MARKDOWN
        params["message"] = markdown_to_text(params["message"])

    def publish_feed(self):
        params = self.prepair_params_feed()
        super().publish_feed(params)
