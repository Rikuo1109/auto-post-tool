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
)
from ..schema.response import (
    PostDetailResponse,
    PostManagementDetailResponse,
    PostManagementMatrixResponse,
    PostManagementUidResponse,
)
from ..services import Service
from router.authenticate import AuthBearer
from router.paginate import Pagination
from utils.enums.common import SortingPostEnum, SortingPostManagementEnum, SortTypeEnum


@api_controller(prefix_or_class="/posts", tags=["Post"], auth=AuthBearer())
class PostController:
    @http_post("/create", response=List[PostManagementUidResponse])
    def create_post(self, request, payload: PostRequest):
        service = Service(request=request)
        return service.create_post_service(data=payload)

    @http_get("/matrix", response=List[PostDetailResponse])
    @paginate(Pagination)
    def view_post_matrix(
        self,
        request,
        sorting: SortingPostEnum = SortingPostEnum.CREATED_AT,
        sort_type: SortTypeEnum = SortTypeEnum.ASC,
        filters: PostFiltersRequest = Query(...),
    ):
        service = Service(request=request)
        return service.get_matrix_post_service(filters=filters, sorting=sorting, sort_type=sort_type)

    @http_get("/{uid}/detail", response=PostDetailResponse)
    def view_post_detail(self, request, uid):
        service = Service(request=request)
        return service.get_detail_post_service(uid=uid)

    @http_post("/{uid}/update")
    def update_post_detail(self, request, uid, payload: PostDetailUpdateRequest):
        service = Service(request=request)
        service.update_post_details_service(uid=uid, data=payload)

    @http_post("/{uid}/remove")
    def remove_post(self, request, uid):
        """
        remove a post
        @uid: post uid
        """
        service = Service(request=request)
        service.remove_post_service(uid=uid)

    @http_post("/{uid}/create/post-management")
    def create_post_management(self, request, uid, payload: PostManagementCreateRequest):
        """
        create one|multy post management from a post
        @uid: post uid
        """
        service = Service(request=request)
        service.create_post_management_service(uid=uid, data=payload)

    @http_get("/{uid}/post-management", response=List[PostManagementMatrixResponse])
    @paginate(Pagination)
    def view_post_management_of_post(
        self,
        request,
        uid,
        sorting: SortingPostManagementEnum = SortingPostManagementEnum.TIME_POSTING,
        sort_type: SortTypeEnum = SortTypeEnum.ASC,
        filters: PostManagementFiltersRequest = Query(...),
    ):
        """
        view all post management created by a post
        @uid: post uid
        """
        service = Service(request=request)
        return service.view_post_management_of_post_service(
            uid=uid, filters=filters, sorting=sorting, sort_type=sort_type
        )

    @http_get("/post-management/matrix", response=List[PostManagementMatrixResponse])
    @paginate(Pagination)
    def view_post_management_matrix(
        self,
        request,
        sorting: SortingPostManagementEnum = SortingPostManagementEnum.TIME_POSTING,
        sort_type: SortTypeEnum = SortTypeEnum.ASC,
        filters: PostManagementFiltersRequest = Query(...),
    ):
        service = Service(request=request)
        return service.get_matrix_post_management_service(filters=filters, sorting=sorting, sort_type=sort_type)

    @http_get("/post-management/{uid}/detail", response=PostManagementDetailResponse)
    def view_post_management_detail(self, request, uid):
        """
        view only one post management
        @uid: post-management uid
        """
        service = Service(request=request)
        return service.view_post_management_detail_service(uid=uid)

    @http_post("/post-management/{uid}/remove")
    def remove_post_management(self, request, uid):
        """
        remove only one post management per time
        @uid: post-management uid
        """
        service = Service(request=request)
        service.remove_post_management_service(uid=uid)

    @http_post("/post-management/{uid}/update")
    def update_post_management(self, request, uid, payload: PostManagementUpdateRequest):
        """
        update only one post management per time
        @uid: post-management uid
        """
        service = Service(request=request)
        service.update_post_management_service(uid=uid, data=payload)

    @http_post("/post-management/{uid}/publish")
    def publish_post_management(self, request, uid):
        """
        publish a post management
        @uid: post-management uid
        """
        service = Service(request=request)
        return service.publish_post_management_service(uid=uid)
