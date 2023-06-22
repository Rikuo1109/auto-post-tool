from datetime import datetime
from typing import List, Optional

from ninja import ModelSchema, Schema

from ..models import Post, PostManagement
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum


class PostContentResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type", "created_at"]


class PostManagementResponseSchema(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "post", "platform", "auto_publish", "time_posting"]
        model_fields_optional = []


class PostDetailResponse(PostContentResponseSchema):
    managements: List[PostManagementResponseSchema]


class PostManagementResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]
        model_fields_optional = []
