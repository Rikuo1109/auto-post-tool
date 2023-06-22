from django.db import transaction

from post_management.models.post import PostManagement


class RemovePostManagementService:
    def __init__(self, uid):
        self.uid = uid

    @transaction.atomic
    def __call__(self):
        return PostManagement.get_by_uid(uid=self.uid).delete()
