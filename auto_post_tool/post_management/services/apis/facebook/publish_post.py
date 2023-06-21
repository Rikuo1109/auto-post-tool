import os

import requests

from . import PAGE_HEADERS


class PublishPostServices:
    def __init__(self, **kwargs):
        self.message = kwargs.get("message", None)
        self.page_id = kwargs.get("page_id", None)
        self.group_id = kwargs.get("group_id", None)
        self.link = kwargs.get("link", None)
        self.path_to_photo = kwargs.get("path_to_photo", "")

    def publish_sample_in_page(self):
        if self.page_id is not None:
            params = {}
            if self.message is not None:
                params["message"] = self.message
            response = requests.post(
                f"""https://graph.facebook.com/{self.page_id}/feed""", headers=PAGE_HEADERS, params=params
            )

    def publish_link_in_page(self):
        """TODO: not done"""
        if self.page_id is not None:
            params = {}
            if self.message is not None:
                params["message"] = self.message
            if self.link is not None:
                params["link"] = self.link
            response = requests.post(
                f"""https://graph.facebook.com/{self.page_id}/feed""", headers=PAGE_HEADERS, params=params
            )

    def publish_image_in_page(self):
        if self.page_id is not None:
            params = {"url": self.path_to_photo}
            if self.message is not None:
                params["message"] = self.message
            response = requests.post(
                f"""https://graph.facebook.com/{self.page_id}/photos""", headers=PAGE_HEADERS, params=params
            )

    def publish_video_in_page(self):
        """TODO: not done"""
        if self.page_id is not None:
            response = requests.post(
                f"""https://graph.facebook.com/{self.page_id}/videos""",
                headers=PAGE_HEADERS,
                params={"url": self.path_to_photo},
            )
