from typing import List

from ninja import Query
from ninja.pagination import paginate
from ninja_extra import api_controller, http_get, http_post

from ..schema.payload import (
    PostDetailUpdateRequest,
    PostFiltersRequest,
    PostManagementCreateRequest,
    PostManagementFiltersRequest,
    PostManagementUpdateRequest,
    PostRequest,
    PostWithImageRequest,
)
from ..schema.response import PostContentResponseSchema, PostDetailResponse, PostManagementResponse
from ..services import Service
from router.authenticate import AuthBearer
from router.paginate import Pagination
from utils.enums.common import SortingPostEnum, SortingPostManagementEnum, SortTypeEnum


@api_controller(prefix_or_class="/posts", tags=["Post"], auth=AuthBearer())
class PostController:
    @http_post("/create")
    def create_new_post(self, request, payload: PostRequest):
        service = Service(request=request)
        service.create_post(data=payload)

    @http_post("/create-image")
    def create_new_post_with_image(self, request, payload: PostWithImageRequest):
        service = Service(request=request)
        service.create_post_with_image(data=payload)

    @http_get("/matrix", response=List[PostDetailResponse])
    @paginate(Pagination)
    def get_view_all(
        self,
        request,
        sorting: str = SortingPostEnum.CREATED_AT,
        sort_type: str = SortTypeEnum.ASC,
        filters: PostFiltersRequest = Query(...),
    ):
        service = Service(request=request)
        return service.get_matrix_post(filters=filters, sorting=sorting, sort_type=sort_type)

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
        """
        remove a post
        @uid: post uid
        """
        service = Service(request=request)
        service.remove_post(uid=uid)

    @http_post("/{uid}/create/post-management")
    def create_post_management(self, request, uid, payload: PostManagementCreateRequest):
        """
        create one|multy post management from a post
        @uid: post uid
        """
        service = Service(request=request)
        service.create_post_management(uid=uid, data=payload)

    @http_post("/post-management/{uid}/remove")
    def remove_post_management(self, request, uid):
        """
        remove only one post management per time
        @uid: post-management uid
        """
        service = Service(request=request)
        return service.remove_post_management(uid=uid)

    @http_get("/post-management/matrix", response=List[PostManagementResponse])
    @paginate(Pagination)
    def get_matrix_post_management(
        self,
        request,
        sorting: str = SortingPostManagementEnum.TIME_POSTING,
        sort_type: str = SortTypeEnum.ASC,
        filters: PostManagementFiltersRequest = Query(...),
    ):
        service = Service(request=request)
        return service.get_matrix_post_management(filters=filters, sorting=sorting, sort_type=sort_type)

    @http_post("/post-management/{uid}/update")
    def update_post_management(self, request, uid, payload: PostManagementUpdateRequest):
        """
        update only one post management per time
        @uid: post-management uid
        """
        service = Service(request=request)
        service.update_post_management(uid=uid, data=payload)
