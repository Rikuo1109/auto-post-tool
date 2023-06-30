from django.conf import settings

import requests
from ..services.required_items_service import RequiredItemsService
from ..services.response_items_service import ResponseItemsService
from ..services.update_status_service import UpdateStatusService
from utils.enums.post import PostManagementStatusEnum
from utils.exceptions import ValidationError


class PagesFacebookApiService:
    def __init__(self, post_management):
        self.post_management = post_management
        user = post_management.post.user
        service = RequiredItemsService(post_management=self.post_management)
        self.page_id = service.load_item(item_key="page_id")
        self.access_token = service.load_item(item_key="access_token")
        self.path = settings.FACEBOOK_API_HOST
        self.image_ids = list()

    def get_feed_in_page(self):
        response = requests.get(
            "/".join([self.path, self.page_id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response

    def prepair_params_feed(self):
        params = {
            "access_token": self.access_token,
            "message": self.post_management.post.content,
            "published": True,
            "attached_media": str([{"media_fbid": image_id} for image_id in self.image_ids]),
        }

        if self.post_management.auto_publish:
            params["published"] = False
            params["scheduled_publish_time"] = self.post_management.time_posting.timestamp()

        return params

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
            "/".join([self.path, self.page_id, "photos"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return self.handle_response(response)

    def publish_feed(self):
        """Permission
        * pages_manage_posts
        * pages_read_engagement
        * page access token
        """
        self.image_ids = []
        for image in self.post_management.post.images.all():
            self.image_ids.append(self.publish_image(source=image.source)["id"])
        params = self.prepair_params_feed()

        response = requests.post(
            "/".join([self.path, self.page_id, "feed"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return_response = self.handle_response(response)

        service = ResponseItemsService(self.post_management)
        service.save_item(item_key="page_post_id", item_value=return_response["id"])
        service = UpdateStatusService(self.post_management)
        service(PostManagementStatusEnum.SUCCESS)
        return return_response

    def prepair_params_interactions(self):
        return {"access_token": self.access_token}

    def get_all_reactions(self):
        try:
            service = ResponseItemsService(self.post_management)
            page_post_id = service.load_item(item_key="page_post_id")
        except ValidationError:
            return 0

        params = self.prepair_params_interactions()

        response = requests.get(
            "/".join([self.path, page_post_id, "reactions"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return_response = self.handle_response(response)
        return len(return_response["data"])

    def get_all_comments(self):
        try:
            service = ResponseItemsService(self.post_management)
            page_post_id = service.load_item(item_key="page_post_id")
        except ValidationError:
            return 0

        params = self.prepair_params_interactions()

        response = requests.get(
            "/".join([self.path, page_post_id, "comments"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

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
