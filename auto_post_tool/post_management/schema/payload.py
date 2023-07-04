from datetime import datetime
from typing import List, Optional

from ninja import Field, FilterSchema, ModelSchema, Schema

from ..models import Post
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum


"""
MODEL SCHEMA FIELDS
"""


class PostPayloadSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["content", "post_type", "created_at"]


class PostManagementPayloadSchema(Schema):
    platform: PostManagementPlatFormEnum
    auto_publish: bool
    time_posting: Optional[datetime]
    required_items: Optional[dict]


"""
CREATE FIELDS
"""


class PostManagementCreateRequest(Schema):
    managements: List[PostManagementPayloadSchema]


class PostRequest(Schema):
    content: Optional[str]
    post_types: List[str] = []
    images: List[str] = []
    managements: List[PostManagementPayloadSchema]


"""
UPDATE FIELDS
"""


class PostDetailUpdateRequest(Schema):
    content: Optional[str]
    post_types: List[str] = []


class PostManagementUpdateRequest(Schema):
    platform: Optional[PostManagementPlatFormEnum]
    auto_publish: Optional[bool]
    time_posting: Optional[datetime]


"""
FILTER FIELDS
"""


class PostFiltersRequest(FilterSchema):
    search: Optional[str] = Field(q=["content__icontains", "post_type__icontains"])
    post_type: Optional[PostTypeEnum] = Field(q=["post_type__iexact"])
    min_time: Optional[datetime] = Field(q=["created_at__gte"])
    max_time: Optional[datetime] = Field(q=["created_at__lte"])


class PostManagementFiltersRequest(FilterSchema):
    platform: Optional[PostManagementPlatFormEnum] = Field(q=["platform__iexact"])
    auto_publish: Optional[bool] = Field(q=["auto_publish__exact"])
    status: Optional[PostManagementStatusEnum] = Field(q=["platform__iexact"])
    min_time: Optional[datetime] = Field(q=["created_at__gte"])
    max_time: Optional[datetime] = Field(q=["created_at__lte"])
