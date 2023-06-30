from django.db import transaction


class RemovePostService:
    def __init__(self, post):
        self.post = post

    @transaction.atomic
    def __call__(self):
        return self.post.delete()
