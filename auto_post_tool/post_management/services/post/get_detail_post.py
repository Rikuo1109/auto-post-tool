from post_management.models.post import Post, PostManagement


class GetDetailPostService:
    def __init__(self, uid):
        self.post = Post.get_by_uid(uid=uid)

    def __call__(self):
        setattr(self.post, "management", PostManagement.filter_by_post(post=self.post))
        return self.post
