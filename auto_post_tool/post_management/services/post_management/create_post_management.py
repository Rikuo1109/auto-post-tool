from post_management.models.post import Post, PostManagement


class CreatePostManagementService:
    def __init__(self, post: Post, managements=[]):
        self.post = post
        self.managements = managements if isinstance(managements, list) else [managements]

    def __call__(self):
        return [
            PostManagement(
                post=self.post, platform=_.platform, auto_publish=_.auto_publish, time_posting=_.time_posting
            ).full_clean()
            for _ in self.managements
        ]
