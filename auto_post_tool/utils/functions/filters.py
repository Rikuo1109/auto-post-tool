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
        raise ValidationError(message_code="VALIDATION_ERROR")
