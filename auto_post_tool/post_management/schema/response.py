from ninja import ModelSchema

from ..models import Post


class PostResponse(ModelSchema):
    class Config:
        model = Post
        model_fields = ("uid",)
