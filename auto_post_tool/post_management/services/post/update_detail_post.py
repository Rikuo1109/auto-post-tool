from django.db import transaction


class UpdatePostDetailService:
    def __init__(self, post, data):
        self.post = post
        self.post.__dict__.update({key: value for key, value in data.dict().items() if value is not None})
        self.content = data.content
        self.post_type = data.post_type

    @transaction.atomic
    def __call__(self):
        self.post.save()
        return self.post
