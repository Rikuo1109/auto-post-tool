from .required_items_service import RequiredItemsService
from ..facebook.pages_api import PagesFacebookApiService
from utils.enums.post import PostManagementPlatFormEnum


class ApiGetInteractionsService:
    def __init__(self, post_management):
        self.post_management = post_management

    def get_all_reactions(self):
        if self.post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            service = RequiredItemsService(self.post_management)
            required_items = service.load_required_items()
            if "page_id" in required_items:
                service = PagesFacebookApiService(post_management=self.post_management)
                return service.get_all_reactions()

    def get_all_comments(self):
        if self.post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            service = RequiredItemsService(self.post_management)
            required_items = service.load_required_items()
            if "page_id" in required_items:
                service = PagesFacebookApiService(post_management=self.post_management)
                return service.get_all_comments()
