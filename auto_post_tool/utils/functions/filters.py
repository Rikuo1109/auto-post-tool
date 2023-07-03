from django.db.models import Q

from utils.enums.common import SortTypeEnum
from utils.exceptions import ValidationError


class FiltersUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_format_sort_type(sorting: str, sort_type: SortTypeEnum):
        if sort_type == SortTypeEnum.ASC:
            return sorting
        elif sort_type == SortTypeEnum.DESC:
            return f"-{sorting}"
        raise ValidationError(message_code="INVALID_FIELD")

    @staticmethod
    def handle_post_management_of_post_filter_dict(key, value):
        if key == "platform":
            return Q(platform__in=value)
        elif key == "auto_publish":
            return Q(auto_publish__exact=value)
        elif key == "status":
            return Q(status__in=value)
        elif key == "min_time":
            return Q(time_posting__gte=value)
        elif key == "max_time":
            return Q(time_posting__lte=value)

    @staticmethod
    def handle_post_filter_dict(key, value):
        if key == "post_type":
            filter = Q()
            post_types = value if isinstance(value, list) else value.split(",")
            for post_type in post_types:
                filter = filter | Q(post_type__icontains=post_type)
            return filter
        elif key == "min_time":
            return Q(created_at__gte=value)
        elif key == "max_time":
            return Q(created_at__lte=value)
        elif key == "search":
            return Q(content__icontains=value)

    @staticmethod
    def filters_translate(filters, handle_function):
        filters_translate = Q()
        for key, value in filters.__dict__.items():
            if value is not None:
                filters_translate = filters_translate & handle_function(key, value)
        return filters_translate
