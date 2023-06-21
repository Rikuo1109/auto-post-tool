from django.db import transaction

from .create_post import CreatePostService
from .create_post_management import CreatePostManagementService
from .get_detail_post import GetDetailPostService
from .get_matrix_post import GetMatrixPostService
from .remove_post import RemovePostService
from .remove_post_management import RemovePostManagementService
from .update_detail_post import UpdatePostDetailService
from .update_post_management import UpdatePostManagementService
from post_management.models.post import PostManagement


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post(self, data):
        post = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)()
        post_managements = CreatePostManagementService(post=post, managements=data.managements)()
        post.save()
        PostManagement.objects.bulk_create(post_managements)
        return post

    def update_post_details(self, uid, data):
        return UpdatePostDetailService(uid=uid, content=data.content, post_type=data.post_type)()

    def get_matrix_post(self):
        return GetMatrixPostService(
            user=self.request.user,
            sorting=self.request.GET.get("sorting", default=["post_type", "created_at"]),
            filters=self.request.GET.get("filters", default={}),
            search=self.request.GET.get("search", default=None),
        )()

    def get_detail_post(self, uid):
        return GetDetailPostService(uid)()

    def remove_post(self, uid):
        return RemovePostService(uid)()

    def create_post_management(self, uid, data):
        return CreatePostManagementService(uid=uid, managements=data.management)()

    def update_post_management(self, uid, data):
        return UpdatePostManagementService(uid=uid, management=data)()

    def remove_post_management(self, uid):
        return RemovePostManagementService(uid=uid)()
