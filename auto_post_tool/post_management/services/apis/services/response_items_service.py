import json

from django.db import transaction


class ResponseItemsService:
    def __init__(self, post_management):
        self.post_management = post_management
        self.response_items = json.loads(self.post_management.response_items or "{}")

    @transaction.atomic
    def save_item(self, item_key, item_value):
        self.response_items[item_key] = item_value
        self.post_management.response_items = json.dumps(self.response_items)
        self.post_management.save()
