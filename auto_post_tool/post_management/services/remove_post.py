from django.db import transaction

from post_management.models.post import Post


class RemovePostService:
    def __init__(self, uid):
        self.uid = uid

    @transaction.atomic
    def __call__(self):
        post = Post.objects.get(uid=self.uid)
        post.delete()
