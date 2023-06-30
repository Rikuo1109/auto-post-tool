from utils.exceptions.exceptions import ValidationError
from django.conf import settings
from .base import BaseValidator


class BaseValidate:
    @staticmethod
    def validate_username(username: str):
        if settings.USERNAME_MINIMUM_LENGTH:
            if not BaseValidator.is_longger_than(
                value=username, max_length=int(settings.USERNAME_MINIMUM_LENGTH)
            ):
                raise ValidationError(message_code="INVALID_USERNAME")
            return True
        return True

    @staticmethod
    def validate_password(password: str):
        if settings.PASSWORD_MINIMUM_LENGTH:
            if not BaseValidator.is_longger_than(
                value=password, max_length=int(settings.PASSWORD_MINIMUM_LENGTH)
            ):
                raise ValidationError(message_code="INVALID_PASSWORD")
            if settings.PASSWORD_MUST_CONTAIN_NUMBER == "False":
                return True
            if not BaseValidator.is_contain_number(value=password):
                raise ValidationError(message_code="INVALID_PASSWORD")
        return True

    @staticmethod
    def validate_name(name: str):
        if settings.NAME_CANT_CONTAIN_NUMBER == "False":
            return True
        if BaseValidator.is_contain_number(value=name):
            raise ValidationError(message_code="INVALID_NAME")
        return True

    @staticmethod
    def validate_email(email: str):
        if not BaseValidator.check_email_format(value=email):
            raise ValidationError(message_code="INVALID_EMAIL")
        return True

    @staticmethod
    def validate_register(data: dict):
        return (
            BaseValidate.validate_name(name=data.get("first_name"))
            and BaseValidate.validate_name(name=data.get("last_name"))
            and BaseValidate.validate_email(email=data.get("email"))
            and BaseValidate.validate_username(username=data.get("username"))
            and BaseValidate.validate_password(password=data.get("password"))
        )

    @staticmethod
    def validate_info(data: dict):
        return (
            BaseValidate.validate_name(name=data.get("first_name"))
            and BaseValidate.validate_name(name=data.get("last_name"))
            and BaseValidate.validate_username(username=data.get("username"))
        )
