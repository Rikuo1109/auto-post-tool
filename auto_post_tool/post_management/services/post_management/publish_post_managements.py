import threading
from typing import List

from post_management.models import PostManagement
from post_management.services.apis.services.api_publish_service import ApiPublishService
from utils.enums.post import PostManagementStatusEnum


class PublishPostManagements:
    def __init__(self, post_managements: List[PostManagement]):
        self.post_managements = post_managements

    def __call__(self):
        response_list = []
        threads = []
        for post_management in self.post_managements:
            thread = threading.Thread(target=self.publish, args=(post_management,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            response_list.append(thread.join())
        return response_list

    def publish(self, post_management: PostManagement):
        service = ApiPublishService(post_management)
        response_service = service()
        response_item = {
            "uid": post_management.uid,
            "message": response_service,
            "status": PostManagementStatusEnum.SUCCESS,
        }
        if "error" in response_service:
            response_item["status"] = PostManagementStatusEnum.FAIL
        return response_item
