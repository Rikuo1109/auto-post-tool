from ninja_extra import api_controller, http_get, http_post, http_put

from ..models.user import User
from ..schema.payload import (
    UserChangePassword,
    UserLoginRequest,
    UserPasswordResetRequest,
    UserRegisterRequest,
    UserUpdateInfoRequest,
    UserPasswordRegisterRequest,
    EmailRequestResponse,
    FacebookConnectResponse,
)
from ..schema.response import GetUserResponse

from utils.services.data_validate import BaseValidate
from router.authenticate import AuthBearer
from token_management.models.token import ResetToken, RegisterToken
from token_management.services.create_facebook_token import FacebookTokenService
from token_management.services.create_login_token import LoginTokenService
from token_management.services.create_reset_token import ResetTokenService
from token_management.services.create_register_token import RegisterTokenService
from utils.exceptions import AuthenticationFailed, NotFound, ValidationError
from utils.mail import MailSenderService
from utils.services.facebook.get_user_info import get_user_fb_page_info


@api_controller(prefix_or_class="users", tags=["User"])
class UserController:
    @http_post("/login")
    def user_login(self, data: UserLoginRequest):
        user = User.get_user_by_email(email=data.email)
        if not user.check_password(data.password):
            raise AuthenticationFailed(message_code="INVALID_EMAIL_PASSWORD")
        user.check_active()
        return {"access_token": LoginTokenService().create_token(user=user)}

    @http_post("/register")
    def user_register(self, data: UserRegisterRequest):
        BaseValidate.validate_register(data=data.dict())
        if User.objects.filter(email=data.email).exists():
            raise ValidationError(message_code="EMAIL_HAS_BEEN_USED")
        User.objects.create_user(first_name=data.first_name, last_name=data.last_name, email=data.email)
        MailSenderService(recipients=[data.email]).send_register_email()
        return True

    @http_put("/register-check")
    def user_register_check(self, data: UserPasswordRegisterRequest):
        try:
            register_token = RegisterToken.objects.get(token=data.token)
        except RegisterToken.DoesNotExist as e:
            raise NotFound(message_code="REGISTER_TOKEN_INVALID_OR_EXPIRED") from e
        if not RegisterTokenService.check_valid(token=register_token):
            raise ValidationError(message_code="REGISTER_TOKEN_INVALID_OR_EXPIRED")
        BaseValidate.validate_password(password=data.password)
        user = register_token.user
        user.set_password(data.password)
        user.is_active = True
        user.save()
        ResetTokenService.deactivate(user)

    @http_get("/get/me", response=GetUserResponse, auth=AuthBearer())
    def get_me(self, request):
        request.user.facebook_status = FacebookTokenService.check_exist_facebook_token(user=request.user)
        return request.user

    @http_put("/update/password", auth=AuthBearer())
    def change_password(self, request, data: UserChangePassword):
        BaseValidate.validate_password(password=data.new_password)
        user = request.user
        if data.current_password == data.new_password:
            raise AuthenticationFailed(message_code="SAME_PASSWORD")
        if not user.check_password(data.current_password):
            raise AuthenticationFailed(message_code="INVALID_PASSWORD")
        user.set_password(data.new_password)
        user.save()

    @http_put("/update/info", auth=AuthBearer())
    def update_info(self, request, data: UserUpdateInfoRequest):
        BaseValidate.validate_info(data=data.dict())
        user = request.user
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.save()

    @http_post("/logout", auth=AuthBearer())
    def logout(self, request):
        LoginTokenService.deactivate(token=request.auth)

    @http_post("/forgot-password")
    def forgot_password(self, data: EmailRequestResponse):
        BaseValidate.validate_email(email=data.email)
        MailSenderService(recipients=[data.email]).send_reset_password_email()
        return True

    @http_put("/reset-password")
    def password_reset_confirm(self, data: UserPasswordResetRequest):
        try:
            reset_token = ResetToken.objects.get(token=data.token)
        except ResetToken.DoesNotExist as e:
            raise NotFound(message_code="RESET_TOKEN_INVALID_OR_EXPIRED") from e
        if not ResetTokenService.check_valid(token=reset_token):
            raise ValidationError(message_code="RESET_TOKEN_INVALID_OR_EXPIRED")
        BaseValidate.validate_password(password=data.password)
        user = reset_token.user
        if user.check_password(data.password):
            raise AuthenticationFailed(message_code="SAME_PASSWORD")
        user.set_password(data.password)
        user.save()
        ResetTokenService.deactivate(token=reset_token)

    @http_post("/connect/facebook", auth=AuthBearer())
    def connect_facebook_token(self, request, data: FacebookConnectResponse):
        FacebookTokenService.get_long_lived_access_token(user=request.user, short_lived_access_token=data.token)

    @http_put("/disconnect/facebook", auth=AuthBearer())
    def disconnect_facebook_token(self, request):
        FacebookTokenService.deactivate(user=request.user)

    @http_get("/get/facebook/page_id", auth=AuthBearer())
    def get_facebook_groupid(self, request):
        access_token = FacebookTokenService.get_token_by_user(user=request.user)
        return get_user_fb_page_info(token=access_token)
