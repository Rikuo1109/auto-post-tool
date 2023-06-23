from django.db import transaction

from .post.create_post import CreatePostService
from .post.get_detail_post import GetDetailPostService
from .post.remove_post import RemovePostService
from .post.update_detail_post import UpdatePostDetailService
from .post_management.create_post_management import CreatePostManagementService
from .post_management.remove_post_management import RemovePostManagementService
from .post_management.update_post_management import UpdatePostManagementService
from post_management.models.post import Post, PostManagement
from utils.functions.filters import FiltersUtils


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post_service(self, data):
        service = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)
        post = service()
        service = CreatePostManagementService(post=post, managements=data.managements)
        service()
        return post

    def update_post_details_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = UpdatePostDetailService(post=post, data=data)
        return service()

    def get_matrix_post_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        return Post.objects.filter(filters.get_filter_expression(), user__exact=self.request.user).order_by(sort_field)

    def get_matrix_post_management_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        posts = Post.filter_by_user(user=self.request.user)
        return PostManagement.objects.filter(filters.get_filter_expression(), post__in=posts).order_by(sort_field)

    def get_detail_post_service(self, uid):
        service = GetDetailPostService(uid)
        return service()

    def remove_post_service(self, uid):
        service = RemovePostService(uid)
        service()

    def create_post_management_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = CreatePostManagementService(post=post, managements=data.managements)
        service()

    def update_post_management_service(self, uid, data):
        post_management = PostManagement.get_by_uid(uid=uid)
        service = UpdatePostManagementService(post_management=post_management, management=data)
        service()

    def remove_post_management_service(self, uid):
        post_management = PostManagement.get_by_uid(uid=uid)
        service = RemovePostManagementService(post_management=post_management)
        return service()
