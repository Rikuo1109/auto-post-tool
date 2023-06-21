from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


from ninja_extra import api_controller, http_get, http_post

from ..models.user import User
from ..schema.payload import (
    UserChangePassword,
    UserLoginRequest,
    UserRegisterRequest,
    UserUpdateInfoRequest,
    UserEmailRequest,
    UserPasswordResetRequest,
)
from ..schema.response import UserResponse
from router.authenticate import AuthBearer
from utils.exceptions import *

from token_management.services.create_login_token import CreateLoginTokenService
from token_management.services.create_reset_token import CreateResetTokenService

from token_management.models.token import LoginToken, ResetToken
from ..services.data_validate import validate, validate_password, validate_info


@api_controller(prefix_or_class="users", tags=["User"])
class UserController:
    @http_post("/login")
    def user_login(self, data: UserLoginRequest):
        try:
            user = User.objects.get(email=data.email)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
        if not user.check_password(data.password):
            raise AuthenticationFailed("Invalid email or password")
        access_token = CreateLoginTokenService().create_login_token(str(user.uid))
        return {"access_token": access_token}

    @http_post("/register", response=UserResponse)
    def user_register(self, data: UserRegisterRequest):
        data = validate(data)
        return User.objects.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            username=data.username,
            password=data.password,
        )

    @http_get("/get/me", response=UserResponse, auth=AuthBearer())
    def get_me(self, request):
        return request.user

    @http_post("/update/password", auth=AuthBearer())
    def change_password(self, request, data: UserChangePassword):
        validate_password(data.password)
        user = request.user
        if data.current_password == data.new_password:
            raise AuthenticationFailed("New password is the same with current password")
        if not user.check_password(data.current_password):
            raise AuthenticationFailed("Current password field is incorrect")
        user.set_password(data.new_password)
        user.save()
        return True

    @http_post("/update/info", auth=AuthBearer())
    def update_info(self, request, data: UserUpdateInfoRequest):
        validate_info(data)
        user = request.user
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.username = data.username
        user.save()
        return True

    @http_post("/logout", auth=AuthBearer())
    def logout(self, request):
        access_token = request.headers.get("authorization", "").split("Bearer ")[-1]
        try:
            token = LoginToken.objects.get(token=access_token)
            token.active = False
            token.deactivate_at = datetime.now()
            token.save()
        except LoginToken.DoesNotExist:
            raise NotFound("Login token not found")

    @http_post("/forgot-password")
    def forgot_password(self, data: UserEmailRequest):
        try:
            user = User.objects.get(email=data.email)
        except User.DoesNotExist:
            raise ValueError("User not found")

        reset_token = CreateResetTokenService().create_reset_token(user)
        reset_link = f"{settings.FRONTEND_HOST_URL}/reset-password/{reset_token}/{reset_token}"

        send_mail(
            subject="Reset your password",
            message=f"Please click on the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data.email],
        )
        return True

    # Reset password
    @http_post("/reset-password")
    def password_reset_confirm(self, data: UserPasswordResetRequest):
        try:
            reset_token = ResetToken.objects.get(token=data.token)
            user = reset_token.user
        except ResetToken.DoesNotExist:
            raise NotFound("Reset Token not found")
        except User.DoesNotExist:
            raise NotFound("User not found")
        user.setpassword(data.password)
        return True
