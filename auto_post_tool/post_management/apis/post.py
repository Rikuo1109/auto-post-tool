from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..models.post import Post, PostManagement
from ..schema.payload import PostDetailUpdateRequest, PostRemoveRequest, PostRequest
from ..schema.response import PostDetailResponse, PostContentResponse, PostManagementResponse
from ..services.create_post import CreatePostService
from ..services.remove_post import RemovePostService
from ..services.update_detail_post import UpdatePostDetailService
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/posts", tags=["Post"])
class PostController:
    @http_post("/create", auth=AuthBearer())
    def create_new_post(self, request, payload: PostRequest):
        create_post = CreatePostService(
            user=request.user, content=payload.content, post_type=payload.post_type, managements=payload.managements
        )
        create_post()

    @http_post("/update", response=PostDetailResponse, auth=AuthBearer())
    def update_post(self, request, payload: PostRequest):
        return
        # post = Post.objects.get(uid=payload.post.uid)
        # update_post_status = post.update(content=payload.post.content, post_type=payload.post.post_type)
        # post_management = PostManagement.objects.get(post=post)
        # update_post_management_status = post_management.update(
        #     platform=payload.post_management.platform, time_posting=payload.post_management.time_posting
        # )

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
