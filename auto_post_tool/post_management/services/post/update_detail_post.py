from django.db import transaction

from post_management.models.post import Post, PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdatePostDetailService:
    def __init__(self, uid, content=None, post_type=None):
        self.uid = uid
        self.content = content
        self.post_type = post_type

    @transaction.atomic
    def __call__(self):
        post = Post.objects.get(uid=self.uid)
        if self.content is not None:
            post.content = self.content
        if self.post_type is not None:
            post.post_type = self.post_type
        post.save()
        return post
