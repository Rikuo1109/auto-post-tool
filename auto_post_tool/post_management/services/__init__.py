from django.db import transaction

from .apis.facebook.get_informations import *
from .apis.facebook.publish_post import *
from .post.create_post import CreatePostService
from .post.get_detail_post import GetDetailPostService
from .post.get_matrix_post import GetMatrixPostService
from .post.remove_post import RemovePostService
from .post.update_detail_post import UpdatePostDetailService
from .post_management.create_post_management import CreatePostManagementService
from .post_management.get_matrix_post_management import GetMatrixPostManagementService
from .post_management.remove_post_management import RemovePostManagementService
from .post_management.update_post_management import UpdatePostManagementService
from post_management.models.post import Post, PostManagement
from utils.enums.post import PostManagementPlatFormEnum, PostManagementStatusEnum, PostTypeEnum


class Service:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create_post(self, data):
        service = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)
        post = service()

        post_managements = CreatePostManagementService(post=post, managements=data.managements)()
        # TODO: Chơi đồ ít thoy
        [post_management.full_clean() for post_management in post_managements]
        PostManagement.objects.bulk_create(post_managements)
        return post

    def update_post_details(self, uid, data):
        service = UpdatePostDetailService(uid=uid, data=data)
        return service()

    def get_matrix_post(self, filters):
        service = GetMatrixPostService(user=self.request.user, filters=filters)
        return service()

    def get_matrix_post_management(self, filters):
        service = GetMatrixPostManagementService(user=self.request.user, filters=filters)
        return service()

    def get_detail_post(self, uid):
        return GetDetailPostService(uid)()

    def remove_post(self, uid):
        return RemovePostService(uid)()

    def create_post_management(self, uid, data):
        post = Post.get_by_uid(uid=uid)
        post_managements = CreatePostManagementService(post=post, managements=data.managements)()
        [post_management.full_clean() for post_management in post_managements]
        PostManagement.objects.bulk_create(post_managements)

    def update_post_management(self, uid, data):
        post_management = UpdatePostManagementService(uid=uid, management=data.dict())()
        post_management.full_clean()
        post_management.save()

    def remove_post_management(self, uid):
        return RemovePostManagementService(uid=uid)()

    def test_facebook_api(self):
        return PublishPostServices(
            message="Hello, welcome to my channel", page_id=111255372005139
        ).publish_sample_in_page()
        return PublishPostServices(
            page_id=111255372005139,
            path_to_photo="https://images.unsplash.com/photo-1629654769983-94d7ad40d4fc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=464&q=80",
            message="Hello Horus Team",
        ).publish_image_in_page()
        return GetInformationServices().get_user_pages()
        return GetInformationServices().get_user_info()
