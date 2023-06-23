from typing import List

from django.shortcuts import render

from ninja import File, NinjaAPI
from ninja.files import UploadedFile
from ninja_extra import api_controller, http_get, http_post

from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/images", tags=["Image"], auth=AuthBearer())
class ImageController:
    @http_post("/upload")
    def upload_image(self, request, file: UploadedFile = File(...)):
        data = file.read()
        return {"name": file.name, "len": len(data)}

    @http_post("/upload-multy")
    def upload_image(self, request, files: List[UploadedFile] = File(...)):
        return [f.name for f in files]


# # Create your views here.
# , images: Optional[Union[UploadedFile, List[UploadedFile]]]

#         # if images:
#         #     images = images if isinstance(images, list) else list(images)
#         #     [Service.generate_image(post, image) for image in images]
