import json

from django.db import transaction

from utils.exceptions import ValidationError


class ResponseItemsService:
    def __init__(self, post_management):
        self.post_management = post_management
        self.response_items = json.loads(self.post_management.response_items or "{}")

    @transaction.atomic
    def save_item(self, item_key, item_value):
        self.response_items[item_key] = item_value
        self.post_management.response_items = json.dumps(self.response_items)
        self.post_management.save()

    def load_response_items(self):
        return self.response_items

    def is_contain_item(self, item_key):
        if item_key in self.response_items:
            return True
        return False

    def load_item(self, item_key):
        if self.is_contain_item(item_key):
            return self.response_items[item_key]
        raise ValidationError("MATERIAL_NOT_FOUND")
