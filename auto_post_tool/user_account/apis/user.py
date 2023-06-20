from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


from ninja_extra import api_controller, http_get, http_post

import jwt
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
from router.authenticate import AuthBearer, BlacklistToken
from utils.exceptions import *


# function to generate JWT token
def generate_jwt_token(user_uid):
    access_token_payload = {
        "user_uid": user_uid,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")

    return access_token


@api_controller(prefix_or_class="users", tags=["User"])
class UserController:
    @http_post("/login")
    def user_login(self, request, data: UserLoginRequest):
        username = data.username
        password = data.password

        try:
            user = User.objects.get(username=username)
        except:
            raise AuthenticationFailed
        if not check_password(password, user.password):
            raise AuthenticationFailed

        access_token = generate_jwt_token(str(user.uid))

        return {"message": "User login successfully!", "access_token": access_token}

    @http_post("/register", response=UserResponse)
    def user_register(self, request, data: UserRegisterRequest):
        first_name = data.first_name
        last_name = data.last_name
        email = data.email
        username = data.username
        password = data.password

        # Create a new user with the given email and password
        return User.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=username, password=password
        )


    @http_get("/get/me", response=UserResponse, auth=AuthBearer())
    def get_me(self, request):
        user = request.user
        return user

    # Changing password
    @http_post("/update/password", auth=AuthBearer())
    def change_password(self, request, data: UserChangePassword):
        user = request.user
        current_password = data.current_password
        new_password = data.new_password
        if current_password == new_password:
            return {"message": "New password is the same with current password"}
        if not check_password(current_password, user.password):
            return {"Error": "Current password field is incorrect"}
        # set new password and save user
        user.set_password(data.new_password)
        user.save()

        return {"message": "Password updated successfully"}

    # Update info
    @http_post("/update/info", auth=AuthBearer())
    def update_info(self, request, data: UserUpdateInfoRequest):
        user = request.user
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.username = data.username
        user.email = data.email
        user.save()

        return {"message": "Info updated successfully"}

    # Update info
    @http_post("/logout", auth=AuthBearer())
    def logout(self, request):
        jwt_token = request.headers.get("authorization", "").split("Bearer ")[-1]
        BlacklistToken.add_token(jwt_token)
        return BlacklistToken.print()

    @http_post("/forgot-password")
    def forgot_password(self, request, data: UserEmailRequest):
        email = data.email

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValueError("Invalid email address")

        # Create reset token
        token_generator = default_token_generator
        uidb64 = urlsafe_base64_encode(force_bytes(user.uid))
        token = token_generator.make_token(user)

        # Generate the reset link
        reset_link = f"{settings.FRONTEND_HOST_URL}/reset-password/{uidb64}/{token}/"

        # Send the reset link in email
        send_mail(
            subject="Reset your password",
            message=f"Please click on the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return {"message": "Email sent successfully"}

    # Reset password
    @http_post("/reset-password")
    def password_reset_confirm(self, request, data: UserPasswordResetRequest):
        try:
            # Decode the id and retrieve the user
            uid = urlsafe_base64_decode(data.uidb64).decode()
            user = User.objects.get(uid=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValueError("Invalid reset link")

        # Verify that the token is valid
        token_generator = default_token_generator
        if not token_generator.check_token(user, data.token):
            raise ValueError("Expired or invalid reset link")

        # Set the new password for the user
        password = data.password
        if not password:
            raise ValueError("New password is required")
        user.set_password(password)
        user.save()

        # Log the user in and redirect to dashboard
        return {"message": "Password reset successful"}
