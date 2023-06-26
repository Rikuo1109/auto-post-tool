from typing import List

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, http_post

from .models import ImagePost
from router.authenticate import AuthBearer
from image_management.schema.response import ImagePostResponseSchema


@api_controller(prefix_or_class="/images", tags=["Image"], auth=AuthBearer())
class ImageController:
    @http_post("/upload", response=ImagePostResponseSchema)
    def upload_image(self, request, file: UploadedFile = File(...)):
        image = ImagePost.objects.create(source=file)
        return image

    @http_post("/upload-multy", response=List[ImagePostResponseSchema])
    def upload_multy_image(self, request, files: List[UploadedFile] = File(...)):
        images = []
        for image in files:
            image = ImagePost(source=image)
            images.append(image)
        return ImagePost.objects.bulk_create(images)
