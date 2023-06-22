import os
from math import floor

from django.db import transaction

from post_management.models.post import Post, PostManagement
from utils.enums.common import SortTypeEnum


class GetMatrixPostManagementService:
    def __init__(self, user, filters):
        self.user = user
        self.filters = filters
        self.default_page_size = int(os.environ.get("DEFAULT_PAGE_SIZE"))

    def filter_paging(self, post_managements):
        offset = (self.filters.page - 1) * self.default_page_size
        offset = min(offset, floor(len(post_managements) / self.default_page_size) * self.default_page_size)
        limit = offset + self.default_page_size
        return post_managements[offset:limit]

    def filter_sorting(self, post_managements):
        sort_type = self.filters.sort_type or SortTypeEnum.ASC
        sort_field = self.filters.sorting
        if sort_type == SortTypeEnum.DESC:
            sort_field = f"-{sort_field}"
        return post_managements.order_by(sort_field)

    def __call__(self):
        post_managements = PostManagement.objects.filter(post__in=Post.objects.filter(user=self.user))
        if self.filters.platform:
            post_managements = post_managements.filter(platform=self.filters.platform)
        if self.filters.auto_publish is not None:
            post_managements = post_managements.filter(auto_publish=self.filters.auto_publish)
        if self.filters.status:
            post_managements = post_managements.filter(status=self.filters.status)
        if self.filters.min_time:
            post_managements = post_managements.filter(time_posting__gte=self.filters.min_time)
        if self.filters.max_time:
            post_managements = post_managements.filter(time_posting__lte=self.filters.max_time)
        post_managements = self.filter_sorting(post_managements)
        return self.filter_paging(post_managements)
