import json

from django.db import transaction


class ResponseItemsService:
    def __init__(self, post_management):
        self.post_management = post_management
        self.response_items = json.loads(self.post_management.response_items)

    @transaction.atomic
    def save_page_post_id(self, page_post_id: str):
        self.response_items["page_post_id"] = page_post_id
        self.post_management.response_items = json.dumps(self.response_items)
        self.post_management.save()

    @transaction.atomic
    def save_group_post_id(self, group_post_id: str):
        self.response_items["group_post_id"] = group_post_id
        self.post_management.response_items = json.dumps(self.response_items)
        self.post_management.save()
