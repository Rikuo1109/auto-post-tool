from django.db import transaction

from post_management.models.post import PostManagement


class CreatePostManagement:
    def __init__(self, post, platform=None, auto_publish=None, time_posting=None):
        self.post = post
        self.platform = platform
        self.auto_publish = auto_publish
        self.time_posting = time_posting

    @transaction.atomic
    def __call__(self):
        post_management = PostManagement(
            post=self.post, platform=self.platform, auto_publish=self.auto_publish, time_posting=self.time_posting
        )
        post_management.save()
