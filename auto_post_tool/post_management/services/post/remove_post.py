from django.db import transaction

from post_management.models.post import Post


class RemovePostService:
    def __init__(self, uid):
        self.uid = uid

    @transaction.atomic
    def __call__(self):
        return Post.objects.get(uid=self.uid).delete()
