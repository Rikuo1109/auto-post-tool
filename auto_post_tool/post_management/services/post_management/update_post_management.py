from django.db import transaction

from post_management.models.post import PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdatePostManagementService:
    def __init__(self, uid, management):
        self.uid = uid
        self.post_management = PostManagement.get_by_uid(uid=self.uid)
        self.platform = management.platform
        self.auto_publish = management.auto_publish
        self.time_posting = management.time_posting
        if self.platform is not None:
            self.post_management.platform = self.platform
        if self.auto_publish is not None:
            self.post_management.auto_publish = self.auto_publish
        if self.time_posting is not None:
            self.post_management.time_posting = self.time_posting

    @transaction.atomic
    def __call__(self):
        return self.post_management
