from django.conf import settings

import requests
from ..services.required_items_service import RequiredItemsService
from ..services.response_items_service import ResponseItemsService
from ..services.update_status_service import UpdateStatusService
from utils.enums.post import PostManagementStatusEnum
from utils.exceptions import ValidationError


def insert_post_to_middle(base_id):
    base_id = base_id.split("_")
    base_id.insert(1, "post")
    return "_".join(base_id)


class BaseFacebookApiService:
    def __init__(self, post_management, base_id):
        self.post_management = post_management
        service = RequiredItemsService(post_management=self.post_management)
        self.base_id = service.load_item(item_key=base_id)
        self.access_token = service.load_item(item_key="access_token")
        self.path = settings.FACEBOOK_API_HOST
        self.image_ids = list()

    def get_feed(self):
        response = requests.get(
            f"{self.path}/{self.base_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def prepair_params_feed(self):
        for image in self.post_management.post.images.all():
            self.image_ids.append(self.publish_image(url=image.url)["id"])

        return {
            "access_token": self.access_token,
            "message": self.post_management.post.content,
            "published": True,
            "attached_media": str([{"media_fbid": image_id} for image_id in self.image_ids]),
        }

    def prepair_params_photos(self, url):
        return {"access_token": self.access_token, "url": url, "published": False, "temporary": True}

    def publish_image(self, url):
        params = self.prepair_params_photos(url=url)

        response = requests.post(f"{self.path}/{self.base_id}/photos", params=params, timeout=settings.REQUEST_TIMEOUT)

        return self.handle_response(response)

    def publish_feed(self, params):
        response = requests.post(f"{self.path}/{self.base_id}/feed", params=params, timeout=settings.REQUEST_TIMEOUT)
        response = self.handle_response(response)

        service = ResponseItemsService(self.post_management)
        service.save_item(item_key=insert_post_to_middle(self.base_id), item_value=response["id"])
        service = UpdateStatusService(post_management=self.post_management, status=PostManagementStatusEnum.SUCCESS)
        service()

        return response

    def get_all_reactions(self):
        try:
            service = ResponseItemsService(self.post_management)
            base_post_id = service.load_item(item_key=insert_post_to_middle(self.base_id))
        except ValidationError:
            return 0

        params = self.prepair_params_interactions()

        response = requests.get(
            f"{self.path}/{base_post_id}/reactions", params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return_response = self.handle_response(response)
        return len(return_response["data"])

    def prepair_params_interactions(self):
        return {"access_token": self.access_token}

    def get_all_comments(self):
        try:
            service = ResponseItemsService(self.post_management)
            base_post_id = service.load_item(item_key=insert_post_to_middle(self.base_id))
        except ValidationError:
            return 0

        params = self.prepair_params_interactions()

        response = requests.get(f"{self.path}/{base_post_id}/comments", params=params, timeout=settings.REQUEST_TIMEOUT)

        return_response = self.handle_response(response)
        return len(return_response["data"])

    def handle_response(self, response):
        """
        handle response does not complete, please check by using response.json()
        print("response", response.json())
        """
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            response_code = response.json().get("error").get("code")
            if response_code == 100:
                raise ValidationError(message_code="INVALID_SCHEDULED_PUBLISH_TIME")
            elif response_code == 190:
                raise ValidationError(message_code="INVALID_FACEBOOK_TOKEN")
        raise ValidationError(message_code="CONTACT_ADMIN_FOR_SUPPORT")
