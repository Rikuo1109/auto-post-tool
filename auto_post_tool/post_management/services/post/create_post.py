from django.db import transaction
from ...schema.payload import PostRequest
from post_management.models.post import Post


class CreatePostService:
    def __init__(self, user, data: PostRequest):
        self.user = user
        self.content = data.content
        self.post_type = data.post_type
        self.title = data.title

    @transaction.atomic
    def __call__(self):
        return Post.objects.create(user=self.user, title=self.title, content=self.content, post_type=self.post_type)
