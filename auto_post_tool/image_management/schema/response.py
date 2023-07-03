from ninja import ModelSchema

from ..models import ImagePost


class ImagePostResponseSchema(ModelSchema):
    url: str

    class Config:
        model = ImagePost
        model_fields = ["uid"]
