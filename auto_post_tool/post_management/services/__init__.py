from django.db import transaction
from django.db.models import Q

from .post.create_post import CreatePostService
from .post.get_detail_post import GetDetailPostService
from .post.remove_post import RemovePostService
from .post.update_detail_post import UpdatePostDetailService
from .post_management.create_post_management import CreatePostManagementService
from .post_management.remove_post_management import RemovePostManagementService
from .post_management.update_post_management import UpdatePostManagementService
from post_management.models.post import Post, PostManagement
from utils.enums.common import SortTypeEnum


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post(self, data):
        service = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)
        post = service()
        service = CreatePostManagementService(post=post, managements=data.managements)
        post_managements = service()
        PostManagement.objects.bulk_create(post_managements)
        return post

    def update_post_details(self, uid, data):
        service = UpdatePostDetailService(uid=uid, data=data)
        return service()

    def get_matrix_post(self, filters, sorting, sort_type):
        sort_field = f"{'' if sort_type is SortTypeEnum.ASC else '-'}{sorting}"
        return Post.objects.filter(Q(user__exact=self.request.user) & filters.get_filter_expression()).order_by(
            sort_field
        )

    def get_matrix_post_management(self, filters, sorting, sort_type):
        sort_field = f"{'' if sort_type is SortTypeEnum.ASC else '-'}{sorting}"
        posts = Post.filter_by_user(user=self.request.user)
        return PostManagement.objects.filter(Q(post__in=posts) & filters.get_filter_expression()).order_by(sort_field)

    def get_detail_post(self, uid):
        service = GetDetailPostService(uid)
        return service()

    def remove_post(self, uid):
        service = RemovePostService(uid)
        service()

    def create_post_management(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        service = CreatePostManagementService(post=post, managements=data.managements)
        post_managements = service()
        PostManagement.objects.bulk_create(post_managements)

    def update_post_management(self, uid, data):
        service = UpdatePostManagementService(uid=uid, management=data)
        post_management = service()
        post_management.full_clean()
        post_management.save()

    def remove_post_management(self, uid):
        service = RemovePostManagementService(uid=uid)
        return service()
