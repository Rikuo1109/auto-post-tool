from ninja import ModelSchema

from ..models import User


class UserResponse(ModelSchema):
    class Config:
        model = User
        model_fields = ("first_name", "last_name", "email", "username", "date_joined")

class UserResponse2(UserResponse):
    facebook_status: bool