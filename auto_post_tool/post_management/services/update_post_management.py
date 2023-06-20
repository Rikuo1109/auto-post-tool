from django.db import transaction

from post_management.models.post import PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdatePostManagementService:
    def __init__(self, post, managements=[]):
        self.post = post
        if not isinstance(managements, list):
            self.managements = list(managements)
        else:
            self.managements = managements

    @transaction.atomic
    def __call__(self):
        managements = PostManagement.objects.filter(uid__in=[_.uid for _ in self.managements])
        for index, management in enumerate(managements):
            if management.status == PostManagementStatusEnum.PENDING and management.auto_publish:
                """post is being in queue"""
            elif management.status == PostManagementStatusEnum.PENDING and management.auto_publish:
                """user is holding"""

            if self.managements[index].status is not None:
                managements[index].status = self.managements[index].status
            if self.managements[index].auto_publish is not None:
                managements[index].auto_publish = self.managements[index].auto_publish
            if self.managements[index].time_posting is not None:
                managements[index].time_posting = self.managements[index].time_posting

        managements.save()
