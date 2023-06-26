from datetime import datetime
from typing import Any, List, Optional

from ninja import ModelSchema, Schema

from ..models import Post, PostManagement
from utils.enums.post import PostManagementPlatFormEnum


class PostContentResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type", "created_at"]


class PostManagementResponseSchema(ModelSchema):
    platform: PostManagementPlatFormEnum
    auto_publish: bool
    time_posting: datetime

    class Config:
        model = PostManagement
        model_fields = ["uid"]


class PostDetailResponse(PostContentResponseSchema):
    pass


class PostManagementResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]
