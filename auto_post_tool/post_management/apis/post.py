from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..models.post import Post
from ..schema.payload import PostRequest, PostDetailUpdateRequest
from ..schema.response import PostResponse
from router.authenticate import AuthBearer

from ..services.create_post import CreatePostService
from ..services.update_detail_post import UpdatePostDetailService


@api_controller(prefix_or_class="/posts", tags=["Post"])
class PostController:
    @http_post("/create", auth=AuthBearer())
    def create_new_post(self, request, payload: PostRequest):
        create_post = CreatePostService(
            user=request.user, content=payload.content, post_type=payload.post_type, managements=payload.managements
        )
        create_post()
        return {"status": "success"}

    @http_post("/update", response=PostResponse, auth=AuthBearer())
    def update_post(self, request, payload: PostRequest):
        return
        # post = Post.objects.get(uid=payload.post.uid)
        # update_post_status = post.update(content=payload.post.content, post_type=payload.post.post_type)
        # post_management = PostManagement.objects.get(post=post)
        # update_post_management_status = post_management.update(
        #     platform=payload.post_management.platform, time_posting=payload.post_management.time_posting
        # )

    @http_get("/matrix", response=List[PostResponse], auth=AuthBearer())
    def get_view_all(self, request):
        posts = Post.objects.filter(user=request.user)
        return posts

    @http_get("/detail", response=PostResponse, auth=AuthBearer())
    def get_view_post(self, request, post_id):
        post = Post.objects.get(uid=post_id)
        return post

    @http_post("/detail/update", response=PostResponse, auth=AuthBearer())
    def update_detail_post(self, request, payload: PostDetailUpdateRequest):
        update_post = UpdatePostDetailService(payload.post_id, payload.content, payload.post_type)
        update_post()
        return Post.objects.get(uid=payload.post_id)
