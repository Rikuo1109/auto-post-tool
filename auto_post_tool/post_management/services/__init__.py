from .create_post import CreatePostService
from .create_post_management import CreatePostManagementService
from .remove_post import RemovePostService
from .update_detail_post import UpdatePostDetailService
from .get_detail_post import GetDetailPostService
from .update_post_management import UpdatePostManagementService
from post_management.models.post import Post, PostManagement


class Service:
    def __init__(self, request):
        self.request = request

    def create_post(self, data):
        post = CreatePostService(user=self.request.user, content=data.content, post_type=data.post_type)()
        CreatePostManagementService(post=post, managements=data.managements)()
        return post

    def update_post_details(self, uid, data):
        return UpdatePostDetailService(uid=uid, content=data.content, post_type=data.post_type)()

    def get_detail_post(self, uid):
        return GetDetailPostService(uid)

    def remove_post(self, uid):
        return RemovePostService(uid)

    def create_post_management(self, uid, data):
        return CreatePostManagementService(post=Post.objects.get(uid=uid), managements=data.management)()

    def update_post_management(self, uid, data):
        return UpdatePostManagementService(post=Post.objects.get(uid=uid), managements=data.management)()
