from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..models.post import Post, PostManagement
from ..schema.payload import PostDetailUpdateRequest, PostRemoveRequest, PostRequest, PostManagementRequest
from ..schema.response import PostDetailResponse
from ..services.create_post import CreatePostService
from ..services.remove_post import RemovePostService
from ..services.update_detail_post import UpdatePostDetailService
from ..services.create_post_management import CreatePostManagement
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/posts", tags=["Post"])
class PostController:
    @http_post("/create", auth=AuthBearer())
    def create_new_post(self, request, payload: PostRequest):
        create_post = CreatePostService(
            user=request.user, content=payload.content, post_type=payload.post_type, managements=payload.managements
        )
        create_post()

    @http_get("/matrix", response=List[PostDetailResponse], auth=AuthBearer())
    def get_view_all(self, request):
        posts = Post.objects.filter(user=request.user)
        for index, post in enumerate(posts):
            posts[index].managements = PostManagement.objects.filter(post=post)
        return posts

    @http_get("/detail", response=PostDetailResponse, auth=AuthBearer())
    def get_view_post(self, request, uid):
        post = Post.objects.get(uid=uid)
        post.managements = PostManagement.objects.filter(post=post)
        return post

    @http_post("/detail/update", auth=AuthBearer())
    def update_detail_post(self, request, payload: PostDetailUpdateRequest):
        update_post = UpdatePostDetailService(
            uid=payload.uid, content=payload.content, post_type=payload.post_type, managements=payload.managements
        )
        update_post()

    @http_post("/detail/remove", auth=AuthBearer())
    def remove_post(self, request, payload: PostRemoveRequest):
        remove_post_ = RemovePostService(uid=payload.uid)
        remove_post_()

    @http_post("/detail/create-management", auth=AuthBearer())
    def create_post_management(self, request, payload: PostManagementRequest):
        post = Post.objects.get(uid=payload.uid)
        create_post_management_ = CreatePostManagement(
            post=post,
            platform=payload.management.platform,
            auto_publish=payload.management.auto_publish,
            time_posting=payload.management.time_posting,
        )
        create_post_management_()
