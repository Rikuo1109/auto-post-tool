from utils.exceptions.exceptions import ValidationError
from django.conf import settings
from .validate_password import PasswordValidate
from .validate_username import UsernameValidate
from .validate_name import NameValidate
from .validate_email import EmailValidate


class BaseValidate:
    @staticmethod
    def validate_username(username: str):
        if not UsernameValidate.check_minimum_length(username=username):
            raise ValidationError(message_code="INVALID_USERNAME")
        return True

    @staticmethod
    def validate_password(password: str):
        if not PasswordValidate.check_minimum_length(password=password):
            raise ValidationError(message_code="INVALID_PASSWORD")
        if settings.PASSWORD_MUST_CONTAIN_NUMBER != "True":
            return True
        if not PasswordValidate.check_contains_number(password=password):
            raise ValidationError(message_code="INVALID_PASSWORD")
        return True

    @staticmethod
    def validate_name(name: str):
        if settings.NAME_CANT_CONTAIN_NUMBER != "True":
            return True
        if NameValidate.check_contains_number(name=name):
            raise ValidationError(message_code="INVALID_NAME")
        return True

    @staticmethod
    def validate_email(email: str):
        if not EmailValidate.check_email_format(email=email):
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
