from ninja import ModelSchema

from ..models import User


class UserResponse(ModelSchema):
    class Config:
        model = User
        model_fields = ("email", "first_name", "last_name")
