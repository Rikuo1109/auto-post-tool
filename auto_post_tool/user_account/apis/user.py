from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from ninja_extra import api_controller, http_get, http_post

import jwt
from ..models.user import User
from ..schema.payload import UserLoginRequest, UserRegisterRequest
from ..schema.response import UserResponse
from router.authenticate import AuthBearer


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

        user = User.objects.get(username=username)

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
        print(request.user)
        return request.user
