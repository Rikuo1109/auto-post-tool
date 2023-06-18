from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..schema.payload import PostSchema
from ..schema.response import PostResponse
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="posts", tags=["Post"])
class PostController:
    @http_get("/view/all", response=PostResponse)
    def get_view_all(self, request):
        return {"mess": "1"}
        return request.get
