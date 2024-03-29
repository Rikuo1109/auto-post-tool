from enum import unique

from django.db.models import TextChoices


@unique
class PostTypeEnum(TextChoices):
    ARTICLE = "ARTICLE", "article"
    COMMERCIAL = "COMMERCIAL", "commercial"
    MARKETING = "MARKETING", "marketing"
    RECRUITMENT = "RECRUITMENT", "recruitment"
    EDUCATION = "EDUCATION", "education"


@unique
class PostManagementStatusEnum(TextChoices):
    SUCCESS = "SUCCESS", "success"
    FAIL = "FAIL", "fail"
    PENDING = "PENDING", "pending"


@unique
class PostManagementPlatFormEnum(TextChoices):
    FACEBOOK = "FACEBOOK", "facebook"
    LINKEDIN = "LINKEDIN", "linkedin"


@unique
class PostTypeFormatEnum(TextChoices):
    MARKDOWN = "MARKDOWN", "markdown"
    PLAINTEXT = "PLAINTEXT", "plaintext"
