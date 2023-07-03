from datetime import datetime
from typing import List, Optional

from ninja import Field, FilterSchema, Schema

from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum


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


class PublishPostManagementRequest(Schema):
    post_uid: str
    managements: List[PostManagementPayloadSchema]


"""
UPDATE FIELDS
"""


class PostDetailUpdateRequest(Schema):
    title: Optional[str]
    content: Optional[str]
    post_type: List[str]


"""
FILTER FIELDS
"""


class PostFiltersRequest(FilterSchema):
    search: Optional[str]
    min_time: Optional[datetime]
    max_time: Optional[datetime]
    post_type: Optional[str]


class PostManagementFiltersRequest(FilterSchema):
    platform: Optional[List[PostManagementPlatFormEnum]] = Field(q=["platform__in"])
    auto_publish: Optional[bool] = Field(q=["auto_publish__exact"])
    status: Optional[List[PostManagementStatusEnum]] = Field(q=["status__in"])
    min_time: Optional[datetime] = Field(q=["time_posting__gte"])
    max_time: Optional[datetime] = Field(q=["time_posting__lte"])
