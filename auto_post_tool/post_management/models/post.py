from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from user_account.models.user import User
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum
from utils.exceptions import NotFound


def validate_platform(value):
    if value not in PostManagementPlatFormEnum.values:
        raise ValidationError("Invalid platform value")


def validate_status(value):
    if value not in PostManagementStatusEnum.values:
        raise ValidationError("Invalid status value")


def validate_post_type(value):
    if value not in PostTypeEnum.values:
        raise ValidationError("Invalid post_type value")


class Post(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="post_fk_user", db_constraint=False, db_column="user_id"
    )
    content = models.TextField()
    post_type = models.CharField(max_length=150, choices=PostTypeEnum.choices, validators=[validate_post_type])
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_by_uid(uid: str):
        try:
            return Post.objects.get(uid=uid)
        except Post.DoesNotExist as e:
            raise NotFound(message_code="POST_NOT_FOUND") from e

    @staticmethod
    def filter_by_user(user):
        try:
            return Post.objects.filter(user=user)
        except Post.DoesNotExist as e:
            raise NotFound(message_code="POST_NOT_FOUND") from e


class PostManagement(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="post_management_fk_post",
        db_constraint=False,
        db_column="post_id",
    )
    platform = models.CharField(
        max_length=16, choices=PostManagementPlatFormEnum.choices, validators=[validate_platform]
    )
    time_posting = models.DateTimeField(auto_now_add=True)
    auto_publish = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=PostManagementStatusEnum.choices, validators=[validate_status])
    url = models.TextField(blank=True)

    @staticmethod
    def get_by_uid(uid: str):
        try:
            return PostManagement.objects.get(uid=uid)
        except PostManagement.DoesNotExist as e:
            raise NotFound(message_code="POST_MANAGEMENT_NOT_FOUND") from e

    @staticmethod
    def filter_by_user(user):
        try:
            return PostManagement.objects.filter(user=user)
        except PostManagement.DoesNotExist as e:
            raise NotFound(message_code="POST_MANAGEMENT_NOT_FOUND") from e

    @staticmethod
    def filter_by_post(post):
        try:
            print("filter post management by post", PostManagement.objects.filter(post=post))
            return PostManagement.objects.filter(post=post)
        except PostManagement.DoesNotExist as e:
            raise NotFound(message_code="POST_MANAGEMENT_NOT_FOUND") from e

    def full_clean(self, exclude=None, validate_unique=True):
        if self.time_posting >= timezone.now():
            self.auto_publish = True
        self.status = PostManagementStatusEnum.PENDING
        super().full_clean(exclude=["post", "status"], validate_unique=validate_unique)
