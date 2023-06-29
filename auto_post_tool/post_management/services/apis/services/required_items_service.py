import json

from utils.exceptions import ValidationError


class RequiredItemsService:
    def __init__(self, post_management):
        self.post_management = post_management
        self.required_items = json.loads(self.post_management.required_items or "{}")

    def load_required_items(self):
        return self.required_items

    def is_contain_item(self, item_key):
        if item_key in self.required_items:
            return True
        return False

    def load_item(self, item_key):
        if self.is_contain_item(item_key):
            return self.required_items[item_key]
        raise ValidationError("MATERIAL_NOT_FOUND")
