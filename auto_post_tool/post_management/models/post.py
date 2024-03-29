import json
from datetime import datetime
from uuid import uuid4

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models

from image_management.models import ImagePost
from user_account.models.user import User
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum
from utils.exceptions import NotFound, ValidationError


class PostTypeField(models.CharField):
    def db_type(self, connection):
        return "str"

    def get_prep_value(self, value):
        if isinstance(value, list):
            value.sort()
            return json.dumps(value)
        return value

    def from_db_value(self, value, expression, connection):
        if isinstance(value, str):
            value = value.replace("'", '"')
            return json.loads(value)
        return value

    def get_db_prep_save(self, value, connection):
        if not value:
            return None
        if isinstance(value, str):
            value = value.split(",")
        return super().get_db_prep_save(value, connection)


class Post(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="post_fk_user", db_constraint=False, db_column="user_id"
    )
    title = models.TextField(max_length=128, blank=True)
    content = models.TextField()
    post_type = PostTypeField(max_length=255, default="[]")
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
        except DjangoValidationError:
            raise ValidationError(message_code="INVALID_UID")

    @staticmethod
    def filter_by_user(user):
        return Post.objects.filter(user=user)


class PostManagement(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="post_management_fk_post",
        db_constraint=False,
        db_column="post_id",
    )
    content = models.TextField()
    platform = models.CharField(max_length=16, choices=PostManagementPlatFormEnum.choices)
    time_posting = models.DateTimeField(auto_now_add=False)
    auto_publish = models.BooleanField()
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
        except DjangoValidationError:
            raise ValidationError(message_code="INVALID_UID")

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
