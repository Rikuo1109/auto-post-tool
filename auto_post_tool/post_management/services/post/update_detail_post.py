from django.db import transaction

from post_management.models.post import Post


class UpdatePostDetailService:
    def __init__(self, uid, data):
        self.uid = uid
        self.content = data.content
        self.post_type = data.post_type

    @transaction.atomic
    def __call__(self):
        # TODO: Nếu uid sai thì sao?
        post = Post.objects.get(uid=self.uid)
        if self.content is not None:
            post.content = self.content
        if self.post_type is not None:
            post.post_type = self.post_type
        post.save()
        return post
