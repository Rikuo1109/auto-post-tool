import json

from utils.exceptions import ValidationError


class RequiredItemsService:
    def __init__(self, post_management):
        self.post_management = post_management
        self.required_items = json.loads(self.post_management.required_items)

    def load_page_id(self):
        if self.required_items is None or "page_id" not in self.required_items:
            raise ValidationError("FACEBOOK_NOT_FOUND_PAGE")
        return self.required_items["page_id"]

    def load_group_id(self):
        if self.required_items is None or "group_id" not in self.required_items:
            raise ValidationError("FACEBOOK_NOT_FOUND_GROUP")
        return self.required_items["group_id"]
