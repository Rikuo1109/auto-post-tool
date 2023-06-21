from django.db import transaction

from post_management.models.post import Post, PostManagement


class CreatePostManagementService:
    def __init__(self, post, managements=[]):
        self.post = post
        if not isinstance(managements, list):
            self.managements = list(managements)
        else:
            self.managements = managements

    @transaction.atomic
    def __call__(self):
        return [
            PostManagement(
                post=self.post, platform=_.platform, auto_publish=_.auto_publish, time_posting=_.time_posting
            )
            for _ in self.managements
        ]
