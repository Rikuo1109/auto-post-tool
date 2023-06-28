from django.conf import settings

import requests
from utils.exceptions import ValidationError


class PagesFacebookApiService:
    def __init__(self, post_management):
        self.post_management = post_management
        user = post_management.post.user
        self.page_id = "111255372005139"
        self.access_token = "EAAECSZAzYmwwBAPWUbkqUCoj8bbZAbdjPZBOZBXNCVWHXFBjLvM3EqapjZAsQZBvoCf0QlrVUz0QpjU6rVEZCa3zjQ1YQEtB7TcVjwoFpYiFLHySQ2yZBHZBnfgwLLWgeyyz3WsqOXt8kL5w3ZC7hqhYFSIUb2Ym4I9owqabxsKTdyFgAKO578674ZBJDCveNQIjsO0eZBHnGA709JFs6RvRE5tgJHmC4BOZB0YsZD"
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
            "url": "https://github.com/tri218138/Horus-Auto-Post-Images/blob/main/" + source.name + "?raw=true",
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
        self.post_management.url = return_response["id"]
        self.post_management.save()
        return return_response

    def prepair_params_interactions(self):
        return {"access_token": self.access_token}

    def get_all_reactions(self):
        if self.post_management.url is None:
            return 0

        params = self.prepair_params_interactions()

        response = requests.get(
            "/".join([self.path, self.post_management.url, "reactions"]),
            params=params,
            timeout=settings.REQUEST_TIMEOUT,
        )

        return_response = self.handle_response(response)
        return len(return_response["data"])

    def get_all_comments(self):
        if self.post_management.url is None:
            return 0

        params = self.prepair_params_interactions()

        response = requests.get(
            "/".join([self.path, self.post_management.url, "comments"]), params=params, timeout=settings.REQUEST_TIMEOUT
        )

        return_response = self.handle_response(response)
        return len(return_response["data"])

    def handle_response(self, response):
        """
        handle response does not complete, please check by using response.json()
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
