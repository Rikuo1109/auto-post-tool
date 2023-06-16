from ninja_extra import api_controller, http_get

from ..schema.response import UserResponse
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="users", tags=["User"], auth=AuthBearer())
class UserController:
    @http_get("/get/me", response=UserResponse)
    def get_me(self, request):
        return request.user
