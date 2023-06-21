from django.db import transaction

from post_management.models.post import Post, PostManagement


class GetMatrixPostService:
    def __init__(self, user, sorting=[], filters={}, search=None):
        self.posts = Post.objects.filter(user=user)
        self.sorting = sorting
        self.filters = filters
        self.search = search

    def filter_by_fields(self, **filters_fields):
        self.posts = self.posts.filter(**filters_fields)

    def sort_by_fields(self, *sorting_fields):
        self.posts = self.posts.order_by(*sorting_fields)

    def search_by_values(self, values=None):
        if isinstance(values, str):
            self.posts = self.posts.filter(content__contains=values)

    @transaction.atomic
    def __call__(self):
        self.filter_by_fields(**self.filters)
        self.sort_by_fields(*self.sorting)
        self.search_by_values(self.search)

        for post in self.posts:
            post.managements = PostManagement.objects.filter(post=post)
        return self.posts
