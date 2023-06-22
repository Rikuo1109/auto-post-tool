from enum import unique

from django.db.models import TextChoices


@unique
class SortTypeEnum(TextChoices):
    ASC = "asc"
    DESC = "desc"


@unique
class SortingPostEnum(TextChoices):
    POST_TYPE = "post_type"
    CREATED_AT = "created_at"

    @classmethod
    def valid_sort_types(cls, field):
        return {
            cls.POST_TYPE: [SortTypeEnum.ASC, SortTypeEnum.DESC],
            cls.CREATED_AT: [SortTypeEnum.ASC, SortTypeEnum.DESC],
        }.get(field, [])
