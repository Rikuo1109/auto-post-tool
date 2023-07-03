from django.conf import settings

import firebase_admin
from firebase_admin import credentials, storage
from image_management.models import ImagePost

cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred, {"storageBucket": settings.FIREBASE_STORAGE_BUCKET})


class FirebaseService:
    def __init__(self):
        pass

    @staticmethod
    def push_image(image, uid, isPublic=True) -> str:
        bucket = storage.bucket()
        blob = bucket.blob(uid)
        image.file.seek(0)
        blob.upload_from_file(image.file, content_type=image.content_type)
        if isPublic:
            blob.make_public()
        return blob.public_url

    @staticmethod
    def create_image(source):
        image = ImagePost()
        image.url = FirebaseService.push_image(image=source, uid=str(image.uid))
        image.save()
        return image
