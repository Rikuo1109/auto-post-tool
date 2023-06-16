from uuid import uuid4

from django.db import models

from user_account.models.user import User
from utils.enums.post import PostManagementStatusEnum, PostTypeEnum, PostManagementPlatFormEnum


class Post(models.Model):
    user = models.ForeignKey(to=User)
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField()
    post_type = models.CharField(max_length=150, choices=PostTypeEnum)
    created_at = models.DateTimeField(auto_now_add=True)


class PostManagement(models.Model):
    post = models.ForeignKey(to=Post)
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum)
    status = models.CharField(max_length=16, choices=PostManagementStatusEnum)
    timePosting = models.DateTimeField(auto_now_add=True)
    autoPublish = models.BooleanField(default=False)
    url = models.TextField()

    def getReactionDetail(self):
        pass

    def setTimePosting(t: models.DateTimeField):
        pass
