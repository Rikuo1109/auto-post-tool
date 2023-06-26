from ninja_extra import api_controller, http_get, http_post, http_put

from ..models.user import User
from ..schema.payload import (
    UserChangePassword,
    UserEmailRequest,
    UserFacebookTokenRequest,
    UserLoginRequest,
    UserPasswordResetRequest,
    UserRegisterRequest,
    UserUpdateInfoRequest,
    UserZaloTokenRequest,
)
from ..schema.response import UserResponse, UserResponse2
from ..services.data_validate import (
    validate_password,
    validate_register,
    validate_update_info,
    validate_update_password,
)
from router.authenticate import AuthBearer
from token_management.models.token import ResetToken
from token_management.services.create_facebook_token import FacebookTokenService
from token_management.services.create_login_token import LoginTokenService
from token_management.services.create_reset_token import ResetTokenService
from token_management.services.create_zalo_token import ZaloTokenService
from utils.exceptions import AuthenticationFailed, NotFound, ValidationError
from utils.mail import MailSenderService


@api_controller(prefix_or_class="users", tags=["User"])
class UserController:
    @http_post("/login")
    def user_login(self, data: UserLoginRequest):
        user = User.get_user_by_email(data.email)
        if not user.check_password(data.password):
            raise AuthenticationFailed(message_code="INVALID_EMAIL_PASSWORD")
        return {"access_token": LoginTokenService().create_token(user)}

    @http_post("/register", response=UserResponse)
    def user_register(self, data: UserRegisterRequest):
        validate_register(data=data.dict())
        if User.objects.filter(email=data.email).exists():
            raise ValidationError(message_code="EMAIL_HAS_BEEN_USED")
        return User.objects.create_user(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password,
        )

    @http_get("/get/me", response=UserResponse2, auth=AuthBearer())
    def get_me(self, request):
        request.user.facebook_status = FacebookTokenService.check_exist_facebook_token(user=request.user)
        request.user.zalo_status = ZaloTokenService.check_exist_zalo_token(user=request.user)
        return request.user

    @http_post("/update/password", auth=AuthBearer())
    def change_password(self, request, data: UserChangePassword):
        validate_update_password(data=data.dict())
        user = request.user
        if data.current_password == data.new_password:
            raise AuthenticationFailed(message_code="SAME_PASSWORD")
        if not user.check_password(data.current_password):
            raise AuthenticationFailed(message_code="INVALID_PASSWORD")
        user.set_password(data.new_password)
        user.save()
        return True

    @http_post("/update/info", auth=AuthBearer())
    def update_info(self, request, data: UserUpdateInfoRequest):
        validate_update_info(data=data.dict())
        user = request.user
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.username = data.username
        user.save()
        return True

    @http_post("/logout", auth=AuthBearer())
    def logout(self, request):
        LoginTokenService.deactivate(token=request.auth)
        return True

    @http_post("/forgot-password")
    def forgot_password(self, data: UserEmailRequest):
        user = User.get_user_by_email(data.email)
        MailSenderService(recipients=[user]).send_reset_password_email()
        return True

    @http_post("/reset-password")
    def password_reset_confirm(self, data: UserPasswordResetRequest):
        try:
            reset_token = ResetToken.objects.get(token=data.token)
        except ResetToken.DoesNotExist as e:
            raise NotFound(message_code="RESET_TOKEN_INVALI_OR_EXPIRED") from e
        if not ResetTokenService.check_valid(reset_token):
            raise ValidationError(message_code="RESET_TOKEN_INVALI_OR_EXPIRED")
        validate_password(password=data.password)
        user = reset_token.user
        user.set_password(data.password)
        user.save()
        ResetTokenService.deactivate(token=reset_token)
        return True

    @http_post("/connect/facebook", auth=AuthBearer())
    def connect_facebook_token(self, request, data: UserFacebookTokenRequest):
        FacebookTokenService.get_long_lived_access_token(request.user, data.token)

    @http_put("/disconnect/facebook", auth=AuthBearer())
    def disconnect_facebook_token(self, request):
        FacebookTokenService.deactivate(request.user)

    @http_post("/connect/zalo", auth=AuthBearer())
    def connect_zalo_token(self, request, data: UserZaloTokenRequest):
        ZaloTokenService.call_access_token_from_oauth(request.user, data.oath_code)

    @http_put("/disconnect/zalo", auth=AuthBearer())
    def disconnect_zalo_token(self, request):
        ZaloTokenService.deactivate(request.user)
