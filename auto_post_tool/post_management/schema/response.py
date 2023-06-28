from typing import List, Optional

from ninja import ModelSchema

from ..models import Post, PostManagement
from image_management.schema.response import ImagePostResponseSchema


class PostContentResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type", "created_at"]


class PostDetailResponse(PostContentResponseSchema):
    images: Optional[List[ImagePostResponseSchema]]


class PostManagementDetailResponse(ModelSchema):
    reactions: Optional[int]
    comments: Optional[int]
    content: str
    images: Optional[List[ImagePostResponseSchema]]

    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]


class PostManagementMatrixResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]


class PostManagementUidResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid"]
