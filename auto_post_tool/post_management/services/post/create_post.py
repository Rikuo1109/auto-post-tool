import json

from django.db import transaction

from post_management.models.post import Post


class CreatePostService:
    def __init__(self, user, data):
        self.user = user
        self.content = data.content
        self.post_type = data.post_type
        self.title = data.title

    @transaction.atomic
    def __call__(self):
        return Post.objects.create(
            user=self.user, title=self.title, content=self.content, post_type=json.dumps(self.post_type)
        )
