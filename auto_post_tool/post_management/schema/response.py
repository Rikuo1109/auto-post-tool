from typing import List, Optional

from ninja import ModelSchema

from ..models import Post, PostManagement
from image_management.schema.response import ImagePostResponseSchema


class PostContentResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type", "created_at"]


class PostManagementResponseSchema(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "post", "platform", "auto_publish", "time_posting"]


class PostDetailResponse(PostContentResponseSchema):
    images: Optional[List[ImagePostResponseSchema]]


class PostManagementResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]
