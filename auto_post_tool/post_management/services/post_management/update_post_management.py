from django.db import transaction

from post_management.models.post import PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdatePostManagementService:
    def __init__(self, uid, management):
        self.uid = uid
        self.post_management = PostManagement.objects.get(uid=self.uid)
        self.platform = management.get("platform", None)
        self.auto_publish = management.get("auto_publish", None)
        self.time_posting = management.get("time_posting", None)
        if self.platform is not None:
            self.post_management.platform = self.platform
        if self.auto_publish is not None:
            self.post_management.auto_publish = self.auto_publish
        if self.time_posting is not None:
            self.post_management.time_posting = self.time_posting

    @transaction.atomic
    def __call__(self):
        return self.post_management
