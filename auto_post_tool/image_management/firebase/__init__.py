from datetime import datetime

from ninja.files import UploadedFile

from image_management.models import ImagePost
from pyrebase import initialize_app
from user_account.models.user import User


config = {
    "apiKey": "AIzaSyDlNprL8t5ElEjMVhu1odD1NfPXJuAOIFg",
    "authDomain": "auto-post-tool.firebaseapp.com",
    "databaseURL": "https://auto-post-tool-default-rtdb.firebaseio.com",
    "projectId": "auto-post-tool",
    "storageBucket": "auto-post-tool.appspot.com",
    "messagingSenderId": "577246572125",
    "appId": "1:577246572125:web:01a77f00606dfe8fe167b4",
    "measurementId": "G-TQQFSL7ZSG",
}

firebase = initialize_app(config)
db = firebase.storage()


class FirebaseService:
    @staticmethod
    def push_image(image, blob_name, isPublic=True) -> str:
        child = db.child(blob_name)
        response = child.put(file=image.file, content_type=image.content_type)
        name = response.get("name").replace("/", "%2F")
        return f"https://firebasestorage.googleapis.com/v0/b/auto-post-tool.appspot.com/o/{name}?alt=media"

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
        file_name, extension = source.name.split(".")
        return f"{user.uid}/{file_name}_{int(datetime.now().timestamp())}.{extension}"
