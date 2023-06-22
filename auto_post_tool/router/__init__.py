from django.conf import settings

from ninja_extra import NinjaExtraAPI
from ninja_extra.operation import Operation

from .exceptions import exception_handler
from .logger import _log_action
from .renderer import Renderer
from user_account.apis import UserController
from post_management.apis import PostController


api = NinjaExtraAPI(
    title=settings.PRODUCT_NAME,
    version=settings.VERSION,
    openapi_url="openapi.json",
    docs_url="docs",
    renderer=Renderer,  # type: ignore
)

Operation._log_action = _log_action  # type: ignore

api.register_controllers(UserController)
api.register_controllers(PostController)

api.add_exception_handler(Exception, exception_handler)  # type: ignore

__all__ = ["api"]
