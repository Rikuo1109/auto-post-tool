from typing import List

from ninja_extra import api_controller, http_get, http_post

from ..schema.payload import LoginSchema
from ..schema.response import UserResponse
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="users", tags=["User"], auth=AuthBearer())
class UserController:
    @http_get("/get/me", response=UserResponse)
    def get_me(self, request):
        return request.user

    @http_post("login")
    def login(self, request, payload: LoginSchema):
        return True
