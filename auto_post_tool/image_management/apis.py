from typing import List

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, http_post

from .models import ImagePost
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/images", tags=["Image"], auth=AuthBearer())
class ImageController:
    @http_post("/upload")
    def upload_image(self, request, file: UploadedFile = File(...)):
        image = ImagePost(source=file)
        image.save()

    @http_post("/upload-multy")
    def upload_images(self, request, files: List[UploadedFile] = File(...)):
        for image in files:
            image = ImagePost(source=image)
            image.save()
