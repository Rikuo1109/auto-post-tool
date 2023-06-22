import os
from math import floor

from django.db import transaction

from post_management.models.post import Post, PostManagement
from utils.enums.common import SortTypeEnum


class GetMatrixPostService:
    def __init__(self, user, filters):
        self.user = user
        self.filters = filters
        self.default_page_size = int(str(os.environ.get("DEFAULT_PAGE_SIZE")))

    def filter_paging(self, posts):
        offset = (self.filters.page - 1) * self.default_page_size
        offset = min(offset, floor(len(posts) / self.default_page_size) * self.default_page_size)
        limit = offset + self.default_page_size
        return posts[offset:limit]

    def filter_sorting(self, posts):
        if self.filters.sorting:
            sort_type = self.filters.sort_type or SortTypeEnum.ASC
            sort_field = self.filters.sorting
            if sort_type == SortTypeEnum.DESC:
                sort_field = f"-{sort_field}"
            return posts.order_by(sort_field)

    @transaction.atomic
    def __call__(self):
        posts = Post.objects.filter(user=self.user)
        if self.filters.post_type:
            posts = posts.filter(post_type=self.filters.post_type)
        if self.filters.min_time:
            posts = posts.filter(created_at__gte=self.filters.min_time)
        if self.filters.max_time:
            posts = posts.filter(created_at__lte=self.filters.max_time)
        posts = self.filter_sorting(posts)
        posts = self.filter_paging(posts)
        for post in posts:
            post.managements = PostManagement.objects.filter(post=post)
        return posts
