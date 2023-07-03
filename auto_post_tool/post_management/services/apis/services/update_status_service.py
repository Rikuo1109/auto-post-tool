from django.db import transaction


class UpdateStatusService:
    def __init__(self, post_management, status):
        self.post_management = post_management
        self.post_management.status = status

    @transaction.atomic
    def __call__(self):
        self.post_management.save()
