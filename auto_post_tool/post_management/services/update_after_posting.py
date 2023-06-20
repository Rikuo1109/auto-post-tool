from django.db import transaction

from post_management.models.post import Post, PostManagement
from utils.enums.post import PostManagementStatusEnum


class UpdateAfterPostingService:
    def __init__(self, uid, status, url):
        self.uid = uid
        self.status = status
        self.url = url

    @transaction.atomic
    def __call__(self):
        post = PostManagement.objects.get(uid=self.uid)
        post_managements = self.modify_exist_managements()
        post.save()
        PostManagement.objects.bulk_update(post_managements, ["status", "auto_publish"]).save()
