import os
from typing import List

from django.conf import settings

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, http_post

from image_management.services import push_image

from .models import ImagePost
from image_management.schema.response import ImagePostResponseSchema
from image_management.services import push_image
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/images", tags=["Image"], auth=AuthBearer())
class ImageController:
    @http_post("/upload", response=ImagePostResponseSchema)
    def upload_image(self, request, file: UploadedFile = File(...)):
        image = ImagePost.objects.create(source=file)
        push_image(file_path=os.path.join(settings.MEDIA_ROOT, image.source.name), file_name=image.source.name)
        return image

    @http_post("/upload-multy", response=List[ImagePostResponseSchema])
    def upload_multy_image(self, request, files: List[UploadedFile] = File(...)):
        images = []
        for image in files:
            image = ImagePost(source=image)
            images.append(image)
        return ImagePost.objects.bulk_create(images)
