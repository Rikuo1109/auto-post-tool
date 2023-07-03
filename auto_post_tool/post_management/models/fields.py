import json

from django.db import models


class PostType(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        return json.loads(value)

    def get_prep_value(self, value):
        if isinstance(value, str):
            return value
        return json.dumps(value)
