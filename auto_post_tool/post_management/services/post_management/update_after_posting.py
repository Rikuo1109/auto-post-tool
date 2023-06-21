from django.db import transaction

from post_management.models.post import Post, PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdatePostManagementAfterPostingService:
    def __init__(self, uid, status, url):
        self.post_management = PostManagement.objects.get(uid=uid)
        self.post_management.status = (
            status if status in PostManagementStatusEnum.choices() else self.post_management.status
        )
        self.post_management.url = url

    @transaction.atomic
    def __call__(self):
        self.post_management.save()
