from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..models.post import Post, PostManagement
from ..schema.payload import PostDetailUpdateRequest, PostManagementRequest, PostManagementUpdateRequest, PostRequest
from ..schema.response import PostDetailResponse
from ..services import Service
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/posts", tags=["Post"], auth=AuthBearer())
class PostController:
    @http_post("/create")
    def create_new_post(self, request, payload: PostRequest):
        service = Service(request=request)
        service.create_post(data=payload)

    @http_get("/matrix", response=List[PostDetailResponse])
    def get_view_all(self, request):
        service = Service(request=request)
        return service.get_matrix_post()

    @http_get("/{uid}/detail", response=PostDetailResponse)
    def get_view_post(self, request, uid):
        service = Service(request=request)
        return service.get_detail_post(uid=uid)

    @http_post("/{uid}/update")
    def update_detail_post(self, request, uid, payload: PostDetailUpdateRequest):
        service = Service(request=request)
        service.update_post_details(uid=uid, data=payload)

    @http_post("/{uid}/remove")
    def remove_post(self, request, uid):
        service = Service(request=request)
        service.remove_post(uid=uid)

    @http_post("/post-management/{uid}/create")
    def create_post_management(self, request, uid, payload: PostManagementRequest):
        service = Service(request=request)
        return service.create_post_management(uid=uid, data=payload)

    @http_post("/post-management/{uid}/remove")
    def create_post_management(self, request, uid):
        service = Service(request=request)
        return service.remove_post_management(uid=uid)

    @http_post("/post-management/{uid}/update")
    def update_post_management(self, request, uid, payload: PostManagementUpdateRequest):
        service = Service(request=request)
        service.update_post_management(uid=uid, data=payload)
