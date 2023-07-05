from datetime import datetime

from ninja.files import UploadedFile

from image_management.models import ImagePost
from pyrebase import initialize_app
from user_account.models.user import User
from django.conf import settings

config = {
    "apiKey": settings.FIREBASE_APIKEY,
    "authDomain": settings.FIREBASE_AUTHDOMAIN,
    "databaseURL": settings.FIREBASE_DATABASEURL,
    "projectId": settings.FIREBASE_PROJECTID,
    "storageBucket": settings.FIREBASE_STORAGEBUCKET,
    "messagingSenderId": settings.FIREBASE_MESSAGINGSENDERID,
    "appId": settings.FIREBASE_APPID,
    "measurementId": settings.FIREBASE_MEASUREMENTID,
}

firebase = initialize_app(config)
db = firebase.storage()


class FirebaseService:
    @staticmethod
    def push_image(image, blob_name) -> str:
        response = db.child(blob_name).put(file=image.file, content_type=image.content_type)
        name = response.get("name").replace("/", "%2F")
        return f"https://firebasestorage.googleapis.com/v0/b/auto-post-tool.appspot.com/o/{name}?alt=media"

    @staticmethod
    def create_image(user: User, source: UploadedFile):
        return ImagePost.objects.create(
            url=FirebaseService.push_image(image=source, blob_name=FirebaseService.generate_image_blob(user, source))
        )

    @staticmethod
    def generate_image_blob(user: User, source: UploadedFile):
        file_name, extension = source.name.split(".")
        return f"{user.uid}/{file_name}_{int(datetime.now().timestamp())}.{extension}"
