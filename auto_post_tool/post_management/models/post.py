from uuid import uuid4

from django.db import models

from user_account.models.user import User
from utils.enums.post import PostManagementStatusEnum, PostTypeEnum, PostManagementPlatFormEnum


class Post(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField()
    post_type = models.CharField(max_length=150, choices=PostTypeEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class PostManagement(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum.choices)
    status = models.CharField(max_length=16, choices=PostManagementStatusEnum.choices)
    time_posting = models.DateTimeField(auto_now_add=True)
    auto_publish = models.BooleanField(default=False)
    url = models.TextField()

    def get_reaction_detail(self):
        pass

    def set_time_posting(t: models.DateTimeField):
        pass
