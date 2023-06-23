from django.db import transaction

from post_management.models.post import Post, PostManagement


class CreatePostManagementService:
    def __init__(self, post: Post, managements=[]):
        self.post = post
        self.managements = managements if isinstance(managements, list) else [managements]

    @transaction.atomic
    def __call__(self):
        post_managements = [
            PostManagement(
                post=self.post, platform=_.platform, auto_publish=_.auto_publish, time_posting=_.time_posting
            )
            for _ in self.managements
        ]
        [_.full_clean() for _ in post_managements]
        return post_managements
