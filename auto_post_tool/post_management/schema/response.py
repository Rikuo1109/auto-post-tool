from ninja import ModelSchema

from ..models import Post, PostManagement
from ninja import Field


class PostContentResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["uid", "content", "post_type", "created_at"]


class PostManagementResponseSchema(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "post", "platform", "auto_publish", "time_posting"]


class PostDetailResponse(PostContentResponseSchema):
    pass


class PostManagementResponse(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["uid", "platform", "auto_publish", "time_posting"]
