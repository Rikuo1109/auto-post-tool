from django.db import transaction


class UpdatePostManagementService:
    def __init__(self, post_management, management):
        self.post_management = post_management
        self.post_management.__dict__.update(
            {key: value for key, value in management.dict().items() if value is not None}
        )

    @transaction.atomic
    def __call__(self):
        self.post_management.full_clean()
        self.post_management.save()
        return self.post_management
