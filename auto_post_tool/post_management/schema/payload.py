from datetime import datetime
from typing import List

from ninja import ModelSchema, Schema

from ..models import Post, PostManagement


class PostPayloadSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["content", "post_type"]


class PostManagementPayloadSchema(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["platform", "auto_publish", "time_posting"]


class PostManagementRequest(Schema):
    management: PostManagementPayloadSchema


class PostRequest(Schema):
    content: str
    post_type: str
    managements: List[PostManagementPayloadSchema]


class PostDetailUpdateRequest(Schema):
    content: str = None
    post_type: str = None


class PostManagementUpdateRequest(Schema):
    platform: str = None
    auto_publish: bool = None
    time_posting: datetime = None
