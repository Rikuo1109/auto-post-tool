import json
from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.db import models

from image_management.models import ImagePost
from user_account.models.user import User
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum
from utils.exceptions import NotFound, ValidationError


class Post(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="post_fk_user", db_constraint=False, db_column="user_id"
    )
    content = models.TextField()
    post_type = models.CharField(max_length=150, default=f"[{settings.DEFAULT_POST_TYPE}]")
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(to=ImagePost, related_name="posts_mm_iamges", blank=True, db_constraint=False)

    @staticmethod
    def get_by_uid(uid: str):
        try:
            return Post.objects.get(uid=uid)
        except Post.DoesNotExist as e:
            raise NotFound(message_code="POST_NOT_FOUND") from e
        except Post.MultipleObjectsReturned as e:
            raise ValidationError(message_code="MORE_THAN_ONE_POST_FOUND") from e

    @staticmethod
    def filter_by_user(user):
        return Post.objects.filter(user=user)

    def set_type_list(self):
        self.post_type = json.loads(self.post_type)


class PostManagement(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="post_management_fk_post",
        db_constraint=False,
        db_column="post_id",
    )
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum.choices)
    time_posting = models.DateTimeField(auto_now_add=False)
    auto_publish = models.BooleanField(default=False)
    status = models.CharField(
        max_length=16, choices=PostManagementStatusEnum.choices, default=PostManagementStatusEnum.PENDING
    )
    url = models.URLField(max_length=255, blank=True)
    required_items = models.TextField(blank=True)
    response_items = models.TextField(blank=True)

    @staticmethod
    def get_by_uid(uid: str):
        try:
            return PostManagement.objects.get(uid=uid)
        except PostManagement.DoesNotExist as e:
            raise NotFound(message_code="POST_MANAGEMENT_NOT_FOUND") from e
        except Post.MultipleObjectsReturned as e:
            raise ValidationError(message_code="MORE_THAN_ONE_POST_MANAGEMENT_FOUND") from e

    @staticmethod
    def filter_by_user(user):
        return PostManagement.objects.filter(user=user)

    @staticmethod
    def filter_by_post(post):
        return PostManagement.objects.filter(post=post)

    def full_clean(self, exclude=["post", "status"], validate_unique=True):
        if self.auto_publish is None:
            raise ValidationError(message_code="INVALID_FIELD")
        if not self.auto_publish:
            self.time_posting = datetime.now()
        elif self.auto_publish and self.time_posting is None:
            raise ValidationError(message_code="INVALID_SCHEDULED_PUBLISH_TIME")
        return super().full_clean(exclude=exclude, validate_unique=validate_unique)
