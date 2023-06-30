from django.db import transaction

from utils.enums.post import PostManagementStatusEnum


class UpdateStatusService:
    def __init__(self, post_management):
        self.post_management = post_management

    @transaction.atomic
    def __call__(self, status: PostManagementStatusEnum):
        self.post_management.status = status
        self.post_management.save()
