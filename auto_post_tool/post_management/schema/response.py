from typing import List, Union

from ninja import Schema, ModelSchema

from ..models import Post, PostManagement


class PostContentResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type"]


class PostManagementResponseSchema(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "post", "platform", "auto_publish", "time_posting"]


class PostDetailResponse(PostContentResponseSchema):
    managements: List[PostManagementResponseSchema]
