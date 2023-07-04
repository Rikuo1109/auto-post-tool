from django.db import transaction


class ContentLogService:
    def __init__(self, post_management, content):
        self.post_management = post_management
        self.post_management.content = content

    @transaction.atomic
    def __call__(self):
        self.post_management.save()
