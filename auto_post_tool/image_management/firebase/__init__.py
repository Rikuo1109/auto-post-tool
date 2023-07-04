from datetime import datetime

from django.conf import settings

from ninja.files import UploadedFile

import firebase_admin
from firebase_admin import credentials, storage
from image_management.models import ImagePost
from user_account.models.user import User


cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred, {"storageBucket": settings.FIREBASE_STORAGE_BUCKET})


class FirebaseService:
    def __init__(self):
        pass

    @staticmethod
    def push_image(image, blob_name, isPublic=True) -> str:
        bucket = storage.bucket()
        blob = bucket.blob(blob_name)
        image.file.seek(0)
        blob.upload_from_file(image.file, content_type=image.content_type)
        if isPublic:
            blob.make_public()
        return blob.public_url

    @staticmethod
    def create_image(user: User, source: UploadedFile):
        image = ImagePost()
        image.url = FirebaseService.push_image(
            image=source, blob_name=FirebaseService.generate_image_blob(user, source)
        )
        image.save()
        return image

    @staticmethod
    def generate_image_blob(user: User, source: UploadedFile):
        return f"{user.uid}/{source.name.split('.')[0]}_{datetime.now().timestamp()}"
