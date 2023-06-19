from uuid import uuid4

from django.db import models
from django.utils import timezone

from user_account.models.user import User
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum


class Post(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField()
    post_type = models.CharField(max_length=150, choices=PostTypeEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def update(self, *args, **kwargs):
        try:
            for field, value in kwargs.items():
                setattr(self, field, value)
                self.save()
            return {"status": "success"}
        except:
            return {"status": "error"}


class PostManagement(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum.choices)
    time_posting = models.DateTimeField(auto_now_add=True)
    auto_publish = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=PostManagementStatusEnum.choices)
    url = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.time_posting < timezone.now():
            pass
        else:
            self.auto_publish = True
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        try:
            for field, value in kwargs.items():
                setattr(self, field, value)
                self.save()
            return {"status": "success"}
        except:
            return {"status": "error"}

    def update_after_posting(self, status, url):
        self.status = status
        self.url = url
