from django.db import transaction

from post_management.models.post import Post, PostManagement


class CreatePostService:
    def __init__(self, user, content, post_type, managements=[]):
        self.user = user
        self.content = content
        self.post_type = post_type
        self.managements = managements

    @transaction.atomic
    def __call__(self):
        post = Post(user=self.user, content=self.content, post_type=self.post_type)

        managements = [
            PostManagement(post=post, platform=_.platform, auto_publish=_.auto_publish) for _ in self.managements
        ]
        post.save()
        PostManagement.objects.bulk_create(managements)
