from django.db import transaction

from .apis import ApiService
from .post import CreatePostService, GetDetailPostService, RemovePostService, UpdatePostDetailService
from .post_management import CreatePostManagementService, RemovePostManagementService, UpdatePostManagementService
from image_management.models import ImagePost
from post_management.models.post import Post, PostManagement
from utils.functions.filters import FiltersUtils


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post_service(self, data):
        service = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)
        post = service()
        if data.images is not None:
            post.images.add(*ImagePost.filter_by_uids(data.images))

        service = CreatePostManagementService(post=post, managements=data.managements)
        post_managements = service()

        service = ApiService(post_managements)
        service.publish_post_management_service()
        return post

    def update_post_details_service(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = UpdatePostDetailService(post=post, data=data)
        return service()

    def get_matrix_post_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        posts = Post.objects.filter(filters.get_filter_expression(), user__exact=self.request.user).order_by(sort_field)
        return posts

    def get_matrix_post_management_service(self, filters, sorting, sort_type):
        sort_field = FiltersUtils.get_format_sort_type(sorting=sorting, sort_type=sort_type)
        posts = Post.filter_by_user(user=self.request.user)
        return PostManagement.objects.filter(filters.get_filter_expression(), post__in=posts).order_by(sort_field)

    def get_detail_post_service(self, uid):
        service = GetDetailPostService(uid)
        post = service()
        return post

    def view_post_management_from_post_service(self, uid):
        return PostManagement.filter_by_post(post=Post.get_by_uid(uid=uid))

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
