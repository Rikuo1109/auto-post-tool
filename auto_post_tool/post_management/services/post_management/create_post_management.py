import json

from django.db import transaction

from post_management.models.post import Post, PostManagement


class CreatePostManagementService:
    def __init__(self, post: Post, managements=[]):
        self.post = post
        self.managements = managements if isinstance(managements, list) else [managements]

    @transaction.atomic
    def __call__(self):
        post_managements = []
        for _ in self.managements:
            post_management = PostManagement(
                post=self.post,
                platform=_.platform,
                auto_publish=_.auto_publish,
                time_posting=_.time_posting,
                required_items=json.dumps(_.required_items),
            )
            post_management.full_clean()
            post_managements.append(post_management)
        PostManagement.objects.bulk_create(post_managements)
        return post_managements
