from ninja import ModelSchema

from ..models import ImagePost


class ImagePostResponseSchema(ModelSchema):
    class Config:
        model = ImagePost
        model_fields = ["uid"]
