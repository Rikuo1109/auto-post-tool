from datetime import datetime

from ninja_extra import api_controller, http_get, http_post

from ..models.user import User
from ..schema.payload import (
    UserChangePassword,
    UserEmailRequest,
    UserLoginRequest,
    UserPasswordResetRequest,
    UserRegisterRequest,
    UserUpdateInfoRequest,
    UserFacebookTokenRequest,
)
from ..schema.response import UserResponse, UserResponse2
from ..services.data_validate import (
    validate_register,
    validate_update_info,
    validate_update_password,
    validate_password,
)
from router.authenticate import AuthBearer
from token_management.models.token import LoginToken, ResetToken, FacebookToken, ZaloToken
from token_management.services.create_login_token import CreateLoginTokenService
from token_management.services.create_reset_token import CreateResetTokenService
from utils.exceptions import AuthenticationFailed, NotFound, ParseError, ValidationError
from utils.mail import MailSenderService
from token_management.services.create_facebook_token import FacebookTokenService


@api_controller(prefix_or_class="users", tags=["User"])
class UserController:
    @http_post("/login")
    def user_login(self, data: UserLoginRequest):
        user = User().get_user_by_email(data.email)
        if not user.check_password(data.password):
            raise AuthenticationFailed(message_code="INVALID_PASSWORD")
        access_token = CreateLoginTokenService().create_token(user)
        return {"access_token": access_token}

    @http_post("/register", response=UserResponse)
    def user_register(self, data: UserRegisterRequest):
        validate_register(data=data.dict())
        return User.objects.create_user(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password,
        )

    @http_get("/get/me", response=UserResponse2, auth=AuthBearer())
    def get_me(self, request):
        request.user.facebook_status = FacebookToken().get_facebook_by_user(request.user)
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
        access_token = request.headers.get("authorization", "").split("Bearer ")[-1]
        CreateLoginTokenService.deactivate(access_token)
        return True

    @http_post("/forgot-password")
    def forgot_password(self, data: UserEmailRequest):
        user = User().get_user_by_email(data.email)
        MailSenderService(user).send_reset_password_email()
        return True

    @http_post("/reset-password")
    def password_reset_confirm(self, data: UserPasswordResetRequest):
        if not data.token:
            raise ParseError(message_code="PARSE_ERROR")
        try:
            reset_token = ResetToken.objects.get(token=data.token)
        except ResetToken.DoesNotExist:
            raise NotFound(message_code="RESET_TOKEN_NOT_FOUND")
        user = reset_token.user
        if not CreateResetTokenService.check_expired(reset_token):
            raise ValidationError(message_code="RESET_TOKEN_EXPIRED")
        validate_password(data.password)
        user.set_password(data.password)
        user.save()
        CreateResetTokenService.deactivate(reset_token)
        return True

    @http_post("/connect/facebook-token", auth=AuthBearer())
    def connect_facebook_token(self, request, data: UserFacebookTokenRequest):
        FacebookTokenService.get_long_lived_access_token(request.user, data.token)

    @http_post("/disconnect/facebook-token", auth=AuthBearer())
    def disconnect_facebook_token(self, request):
        FacebookTokenService.deactivate(request.user)
