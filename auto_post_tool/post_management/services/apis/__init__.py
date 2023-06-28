from .facebook import GroupsFacebookApiService, PagesFacebookApiService
from utils.enums.post import FacebookPlatFormEnum, PostManagementPlatFormEnum


class ApiPublishService:
    def __init__(self, post_management):
        self.post_management = post_management

    def __call__(self):
        """
        Publish post base on platform: FACEBOOK, ZALO
        FACEBOOK:
        * Personal to group
        * Page to group
        * Page to page
        NOTE: scheduled_publish_time (unix_timestamp, from 10 minutes to 75 days) just available in pages
        NOTE: formatting just available in groups
        NOTE: if not auto_post: not publish anywhere
            else if time_posting < now() -> publish rightnow
            else -> schedule for posting
        """
        if self.post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            select = FacebookPlatFormEnum.PAGE
            if select == FacebookPlatFormEnum.PAGE:
                service = PagesFacebookApiService(post_management=self.post_management)
                return service.publish_feed()
            elif select == FacebookPlatFormEnum.GROUP:
                service = GroupsFacebookApiService(post_management=self.post_management)
                return service.publish_feed()
