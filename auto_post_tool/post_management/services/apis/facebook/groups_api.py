from django.conf import settings

import requests
from ..services.required_items_service import RequiredItemsService
from ..services.response_items_service import ResponseItemsService
from ..services.update_status_service import UpdateStatusService
from utils.enums.post import PostManagementStatusEnum, PostTypeFormatEnum
from utils.exceptions import ValidationError


class GroupsFacebookApiService:
    def __init__(self, post_management):
        self.post_management = post_management
        user = post_management.post.user
        service = RequiredItemsService(post_management=self.post_management)
        self.group_id = service.load_item(item_key="group_id")
        self.access_token = service.load_item(item_key="access_token")
        self.path = settings.FACEBOOK_API_HOST
        self.image_ids = list()

    def get_users(self):
        response = requests.get(
            "/".join([self.path, self.group_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def prepair_params_feed(self):
        return {
            "access_token": self.access_token,
            "message": self.post_management.post.content,
            "formatting": PostTypeFormatEnum.MARKDOWN,
            "attached_media": [{"media_fbid": image_id} for image_id in self.image_ids],
        }

    def prepair_params_photos(self, source):
        return {
            "access_token": self.access_token,
            "url": f"https://github.com/{settings.GITHUB_REPO}/blob/main/" + source.name + "?raw=true",
            "published": False,
            "temporary": True,
        }

    def publish_image(self, source):
        params = self.prepair_params_photos(source=source)

        response = requests.post(
            "/".join([self.path, self.group_id, "photos"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return self.handle_response(response)

    def publish_feed(self):
        """
        Facebook's group does not support scheduled_publish_time
        """
        self.image_ids = []
        for image in self.post_management.post.images.all():
            self.image_ids.append(self.publish_image(source=image.source)["id"])
        params = self.prepair_params_feed()

        response = requests.post(
            "/".join([self.path, self.group_id, "feed"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return_response = self.handle_response(response)

        service = ResponseItemsService(self.post_management)
        service.save_item(item_key="group_post_id", item_value=return_response["id"])
        service = UpdateStatusService(self.post_management)
        service(PostManagementStatusEnum.SUCCESS)
        return return_response

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            response_code = response.json().get("error").get("code")
            if response_code == 190:
                raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")
            if response_code == 200:
                raise ValidationError(message_code="USER_DOES_NOT_HAVE_PERMISSIONS")
        raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
