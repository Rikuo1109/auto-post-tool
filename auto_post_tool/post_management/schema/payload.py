from typing import List

from ninja import Schema, ModelSchema
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
    uid: str
    management: PostManagementPayloadSchema


class PostRequest(Schema):
    content: str
    post_type: str
    managements: List[PostManagementPayloadSchema]


class PostDetailUpdateRequest(Schema):
    uid: str
    content: str = None
    post_type: str = None
    managements: List[str] = list()


class PostRemoveRequest(Schema):
    uid: str
