from post_management.services.apis.facebook.pages_api import PagesFacebookApiService
from utils.enums.post import FacebookPlatFormEnum, PostManagementPlatFormEnum


class GetInteractionsService:
    def __init__(self, post_management):
        self.post_management = post_management

    def get_all_reactions(self):
        if self.post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            select = FacebookPlatFormEnum.PAGE
            if select == FacebookPlatFormEnum.PAGE:
                service = PagesFacebookApiService(post_management=self.post_management)
                return service.get_all_reactions()

    def get_all_comments(self):
        if self.post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            select = FacebookPlatFormEnum.PAGE
            if select == FacebookPlatFormEnum.PAGE:
                service = PagesFacebookApiService(post_management=self.post_management)
                return service.get_all_comments()
