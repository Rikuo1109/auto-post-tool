from datetime import datetime
from typing import List, Optional

from ninja import FilterSchema, ModelSchema, Schema

from ..models import Post, PostManagement
from pydantic import Field
from utils.enums.common import SortingPostManagementEnum, SortTypeEnum
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum


"""
MODEL SCHEMA FIELDS
"""


class PostPayloadSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ["content", "post_type", "created_at"]


class PostManagementPayloadSchema(ModelSchema):
    class Config:
        model = PostManagement
        model_fields = ["platform", "auto_publish", "time_posting"]


"""
CREATE FIELDS
"""


class PostManagementCreateRequest(Schema):
    managements: List[PostManagementPayloadSchema]


class PostRequest(Schema):
    content: str
    post_type: PostTypeEnum
    managements: List[PostManagementPayloadSchema]


"""
UPDATE FIELDS
"""


class PostDetailUpdateRequest(Schema):
    content: Optional[str]
    post_type: Optional[PostTypeEnum]


class PostManagementUpdateRequest(Schema):
    platform: Optional[PostManagementPlatFormEnum]
    auto_publish: Optional[bool] = None
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
