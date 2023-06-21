from django.db import transaction

from post_management.models.post import PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdatePostManagementService:
    def __init__(self, uid, management):
        self.uid = uid
        self.post_management = PostManagement.objects.get(uid=self.uid)
        self.post_management.platform = (
            management.platform if management.platform is not None else self.post_management.platform
        )
        self.post_management.auto_publish = (
            management.auto_publish if management.auto_publish is not None else self.post_management.auto_publish
        )
        self.post_management.time_posting = (
            management.time_posting if management.time_posting is not None else self.post_management.time_posting
        )

    @transaction.atomic
    def __call__(self):
        return self.post_management
