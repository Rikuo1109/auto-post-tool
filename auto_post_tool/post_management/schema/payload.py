from datetime import datetime
from typing import List, Optional

from ninja import Field, FilterSchema, ModelSchema, Schema

from ..models import Post
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum


"""
MODEL SCHEMA FIELDS
"""


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
    title: str
    content: Optional[str]
    post_type: List[str]
    images: List[str] = []
    managements: List[PostManagementPayloadSchema]


"""
UPDATE FIELDS
"""


class PostDetailUpdateRequest(Schema):
    title: Optional[str]
    content: Optional[str]
    post_type: Optional[PostTypeEnum]


"""
FILTER FIELDS
"""


class PostFiltersRequest(FilterSchema):
    search: Optional[str] = Field(q=["content__icontains"])
    min_time: Optional[datetime] = Field(q=["created_at__gte"])
    max_time: Optional[datetime] = Field(q=["created_at__lte"])
    post_type: Optional[List[str]]


class PostManagementFiltersRequest(FilterSchema):
    platform: Optional[List[PostManagementPlatFormEnum]] = Field(q=["platform__in"])
    auto_publish: Optional[bool] = Field(q=["auto_publish__exact"])
    status: Optional[List[PostManagementStatusEnum]] = Field(q=["status__in"])
    min_time: Optional[datetime] = Field(q=["time_posting__gte"])
    max_time: Optional[datetime] = Field(q=["time_posting__lte"])
