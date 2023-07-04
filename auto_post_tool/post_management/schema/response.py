from typing import List, Optional

from ninja import ModelSchema

from ..models import Post, PostManagement
from image_management.schema.response import ImagePostResponseSchema


class PostUidResponse(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid"]


class PostContentResponseSchema(ModelSchema):
    post_type: List[str]

    class Config:
        model = Post
        model_fields = ["uid", "title", "content", "created_at"]


class PostManagementMatrixResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting", "status"]


class PostDetailResponse(PostContentResponseSchema):
    managements: Optional[List[PostManagementMatrixResponse]]
    images: Optional[List[ImagePostResponseSchema]]


class PostMatrixResponse(ModelSchema):
    post_type: List[str]

    class Config:
        model = Post
        model_fields = ["uid", "title", "post_type", "created_at"]


class PostManagementDetailResponse(ModelSchema):
    reactions: Optional[int]
    comments: Optional[int]
    title: str
    images: Optional[List[ImagePostResponseSchema]]

    class Config:
        model = PostManagement
        model_fields = ["uid", "content", "platform", "auto_publish", "time_posting", "status"]
