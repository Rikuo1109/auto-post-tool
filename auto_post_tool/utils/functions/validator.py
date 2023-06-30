from post_management.models.post import Post, PostManagement
from user_account.models import User
from utils.exceptions import ValidationError


class ValidatorsUtils:
    def __init__(self):
        pass

    @staticmethod
    def validator_user_post(user: User, post: Post):
        if post.user != user:
            raise ValidationError(message_code="NOT_FOUND")

    @staticmethod
    def validator_user_post_management(user: User, post_management: PostManagement):
        if post_management.post.user != user:
            raise ValidationError(message_code="NOT_FOUND")
