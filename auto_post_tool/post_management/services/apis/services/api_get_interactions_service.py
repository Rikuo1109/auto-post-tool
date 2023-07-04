from ..facebook.pages_api import PagesFacebookApiService
from ..facebook.groups_api import GroupsFacebookApiService
from .required_items_service import RequiredItemsService
from utils.enums.post import PostManagementPlatFormEnum


class ApiGetInteractionsService:
    def __init__(self, post_management):
        self.post_management = post_management
        self.reactions = []
        self.comments = []
        self.shares = []

    def __call__(self):
        if self.post_management.platform == PostManagementPlatFormEnum.FACEBOOK:
            service = RequiredItemsService(self.post_management)
            required_items = service.load_required_items()
            service = None
            if "page_id" in required_items:
                service = PagesFacebookApiService(post_management=self.post_management)
            elif "group_id" in required_items:
                service = GroupsFacebookApiService(post_management=self.post_management)
            if service is None:
                return
            data = service.get_all_insights()
            self.reactions = data.get("reactions", {}).get("data", {})
            self.comments = data.get("comments", {}).get("data", {})
            self.shares = data("shares", {}).get("data", {})

    def get_all_reactions(self):
        return self.reactions

    def get_all_comments(self):
        return self.comments

    def get_all_shares(self):
        return self.shares
