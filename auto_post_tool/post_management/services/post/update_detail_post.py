from django.db import transaction

from post_management.models.post import Post, PostManagement


class UpdatePostDetailService:
    def __init__(self, uid, data):
        self.uid = uid
        self.content = data.get("content", None)
        self.post_type = data.get("post_type", None)

    @transaction.atomic
    def __call__(self):
        post = Post.objects.get(uid=self.uid)
        if self.content is not None:
            post.content = self.content
        if self.post_type is not None:
            post.post_type = self.post_type
        return post
