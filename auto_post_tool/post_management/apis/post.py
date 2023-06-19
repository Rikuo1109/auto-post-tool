from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..models.post import Post, PostManagement
from ..schema.payload import PostRequest
from ..schema.response import PostResponse
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="users/posts", tags=["Post"])
class PostController:
    @http_post("/create", response=PostResponse, auth=AuthBearer())
    def create_new_post(self, request, payload: PostRequest):
        print(request.user)
        post = Post.objects.create_post(
            user=request.user, content=payload.post.content, post_type=payload.post.post_type
        )
        post_management = PostManagement(
            post=post, platform=payload.post_management.platform, time_posting=payload.post_management.time_posting
        )
        if post_management.auto_publish is True:
            """push post_management to priority queue"""
        return post

    @http_post("/update", response=PostResponse, auth=AuthBearer())
    def update_post(self, request, payload: PostRequest):
        post = Post.objects.get(uid=payload.post.uid)
        update_post_status = post.update(content=payload.post.content, post_type=payload.post.post_type)
        post_management = PostManagement.objects.get(post=post)
        update_post_management_status = post_management.update(
            platform=payload.post_management.platform, time_posting=payload.post_management.time_posting
        )

    @http_get("/view/all", response=PostResponse, auth=AuthBearer())
    def get_view_all(self, request):
        posts = Post.objects.filter(user=request.user)
        return posts

    @http_get("/view", response=PostResponse, auth=AuthBearer())
    def get_view_post(self, request, post_id):
        post = Post.objects.filter(user=request.user).get(uid=post_id)
        return post
