from django.db import transaction

from post_management.models.post import PostManagement


class CreatePostManagement:
    def __init__(self, post, managements=[]):
        self.post = post
        self.managements = managements

    @transaction.atomic
    def __call__(self):
        if type(self.managements) is not list:
            self.managements = list(self.managements)
        managements = [
            PostManagement(
                post=self.post, platform=_.platform, auto_publish=_.auto_publish, time_posting=_.time_posting
            )
            for _ in self.managements
        ]
        PostManagement.objects.bulk_create(managements)
