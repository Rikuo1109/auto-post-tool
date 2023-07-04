from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, http_post

from image_management.firebase import FirebaseService
from image_management.schema.response import ImagePostResponseSchema
from router.authenticate import AuthBearer


@api_controller(prefix_or_class="/images", tags=["Image"], auth=AuthBearer())
class ImageController:
    @http_post("/upload", response=ImagePostResponseSchema)
    def upload_image(self, request, file: UploadedFile = File(...)):
        service = FirebaseService()
        return service.create_image(user=request.user, source=file)
