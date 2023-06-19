from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password

from ninja_extra import api_controller, http_get, http_post

import jwt
from ..models.user import User
from ..schema.payload import UserChangePassword, UserLoginRequest, UserRegisterRequest, UserUpdateInfoRequest
from ..schema.response import UserResponse
from router.authenticate import AuthBearer, BlacklistToken
from utils.exceptions import *


# function to generate JWT token
def generate_jwt_token(user_id):
    access_token_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')

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

        access_token = generate_jwt_token(user.id)

        return {
        "message": "User login successfully!",
        "access_token": access_token
        }

    @http_post("/register", response=UserResponse)
    def user_register(self, request, data: UserRegisterRequest):
        first_name = data.first_name
        last_name = data.last_name
        email = data.email
        username = data.username
        password = data.password

        # Create a new user with the given email and password
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

        return user

    @http_get("/get/me", response=UserResponse, auth=AuthBearer())
    def get_me(self, request):
        user = request.user
        return {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "date_joined": user.date_joined
        }

    #Changing password
    @http_post("/update/password", auth=AuthBearer())
    def change_password(self, request, data: UserChangePassword):
        user = request.user
        current_password = data.current_password
        new_password = data.new_password
        if current_password == new_password:
            return {"message":"New password is the same with current password"}
        if not check_password(current_password, user.password):
            return {
                "Error":"Current password field is incorrect"
            }
        # set new password and save user
        user.set_password(data.new_password)
        user.save()

        return {
            "message": "Password updated successfully"
        }
    
    #Update info
    @http_post("/update/info", auth=AuthBearer())
    def update_info(self, request, data: UserUpdateInfoRequest):
        user = request.user
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.username = data.username
        user.email = data.email
        user.save()

        return {
            "message": "Info updated successfully"
        }
    
    #Update info
    @http_post("/logout", auth=AuthBearer())
    def logout(self, request):
        jwt_token = request.headers.get('authorization', '').split('Bearer ')[-1]
        BlacklistToken.add_token(jwt_token)
        return BlacklistToken.print()
