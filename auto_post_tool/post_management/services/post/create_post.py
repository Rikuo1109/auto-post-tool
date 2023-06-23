from django.db import transaction

from post_management.models.post import Post


class CreatePostService:
    def __init__(self, user, content, post_type):
        self.user = user
        self.content = content
        self.post_type = post_type

    @transaction.atomic
    def __call__(self):
        return Post.objects.create(user=self.user, content=self.content, post_type=self.post_type)
