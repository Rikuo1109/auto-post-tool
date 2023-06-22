from django.db import transaction

from post_management.models.post import Post, PostManagement


class GetDetailPostService:
    def __init__(self, uid):
        self.uid = uid

    @transaction.atomic
    def __call__(self):
        post = Post.get_by_uid(uid=self.uid)
        post.managements = PostManagement.filter_by_post(post=post)
        return post
