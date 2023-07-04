from .base_api import BaseFacebookApiService


class PagesFacebookApiService(BaseFacebookApiService):
    def __init__(self, post_management):
        super().__init__(post_management=post_management, base_id="page_id")

    def prepair_params_feed(self):
        params = super().prepair_params_feed()
        if self.post_management.auto_publish:
            params["published"] = False
            params["scheduled_publish_time"] = self.post_management.time_posting.timestamp()
        return params

    def publish_feed(self):
        params = self.prepair_params_feed()
        super().publish_feed(params)
