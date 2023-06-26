from datetime import datetime
from typing import List, Optional

from ninja import ModelSchema

from ..models import Post, PostManagement
from image_management.schema.response import ImagePostResponseSchema
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
    images: Optional[List[ImagePostResponseSchema]]


class PostManagementResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]
