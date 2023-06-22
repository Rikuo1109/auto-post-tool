import os
from datetime import datetime
from typing import List, Optional

from ninja import FilterSchema, ModelSchema, Schema

from ..models import Post, PostManagement
from pydantic import Field, validator
from utils.enums.common import SortingPostEnum, SortingPostManagementEnum, SortTypeEnum
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
        # model_fields_optional = []


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
    page: Optional[int] = 1
    sorting: Optional[SortingPostEnum] = SortingPostEnum.CREATED_AT
    sort_type: Optional[SortTypeEnum] = SortTypeEnum.ASC
    search: Optional[str] = Field(q=["content__icontains", "post_type__icontains"])
    post_type: Optional[PostTypeEnum]
    min_time: Optional[datetime] = None
    max_time: Optional[datetime] = None


class PostManagementFiltersRequest(FilterSchema):
    sorting: Optional[SortingPostManagementEnum] = SortingPostManagementEnum.TIME_POSTING
    sort_type: Optional[SortTypeEnum] = SortTypeEnum.ASC
    page: Optional[int] = 1
    platform: Optional[PostManagementPlatFormEnum]
    auto_publish: Optional[bool] = None
    status: Optional[PostManagementStatusEnum]
    min_time: Optional[datetime] = None
    max_time: Optional[datetime] = None
