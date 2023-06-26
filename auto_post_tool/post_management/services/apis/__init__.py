from .facebook import GroupsFacebookApiService, PagesFacebookApiService
from utils.enums.post import FacebookPlatFormEnum, PostManagementPlatFormEnum


class ApiService:
    def __init__(self, post_managements):
        self.post_managements = post_managements if isinstance(post_managements, list) else list(post_managements)

    def publish_post_management_service(self):
        """
        Publish post base on platform: FACEBOOK, ZALO
        FACEBOOK:
        * Personal to group
        * Page to group
        * Page to page
        scheduled_publish_time (unix_timestamp, from 10 minutes to 75 days) just available in pages
        formatting just available in groups
        """
        for post_management in self.post_managements:
            if post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
                select = FacebookPlatFormEnum.PAGE
                if select == FacebookPlatFormEnum.PAGE:
                    service = PagesFacebookApiService(post_management=post_management)
                    return service.publish_feed()
                elif select == FacebookPlatFormEnum.GROUP:
                    service = GroupsFacebookApiService(post_management=post_management)
                    return service.publish_feed()
