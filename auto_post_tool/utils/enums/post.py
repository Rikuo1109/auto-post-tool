from enum import unique

from django.db.models import TextChoices


@unique
class PostTypeEnum(TextChoices):
    ARTICLE = "ARTICLE", "article"
    COMMERCIAL = "COMMERCIAL", "commercial"
    MARKETING = "MARKETING", "marketing"
    EDUCATION = "EDUCATION", "education"
    RECRUITMENT = "RECRUITMENT", "recruitment"


@unique
class PostManagementStatusEnum(TextChoices):
    SUCCESS = "SUCCESS", "success"
    FAIL = "FAIL", "fail"
    PENDING = "PENDING", "pending"


@unique
class PostManagementPlatFormEnum(TextChoices):
    FACEBOOK = "FACEBOOK", "facebook"
    ZALO = "ZALO", "zalo"