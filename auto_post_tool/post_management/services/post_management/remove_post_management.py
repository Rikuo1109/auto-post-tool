from django.db import transaction

from post_management.models.post import PostManagement


class RemovePostManagementService:
    def __init__(self, post_management):
        self.post_management = post_management

    @transaction.atomic
    def __call__(self):
        return self.post_management.delete()
