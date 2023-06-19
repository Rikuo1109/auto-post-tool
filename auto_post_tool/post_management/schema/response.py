from typing import List, Union

from ninja import Schema, ModelSchema

from ..models import Post, PostManagement


class PostContentResponse(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type"]


class PostManagementResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["platform", "auto_publish"]


class PostDetailResponse(Schema):
    content: PostContentResponse
    managements: List[PostManagementResponse]
