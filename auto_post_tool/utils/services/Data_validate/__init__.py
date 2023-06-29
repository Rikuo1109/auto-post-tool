from ._abstract import StringValidate
from utils.exceptions.exceptions import ValidationError


class BaseValidate:
    @staticmethod
    def validate_username(username: str):
        result = StringValidate.check_minimum_length(input=username)
        if not result:
            raise ValidationError(message_code="INVALID_USERNAME")
        return result

    @staticmethod
    def validate_password(password: str):
        result = StringValidate.check_minimum_length(
            input=password
        ) and StringValidate.check_contains_number_and_letter(input=password)
        if not result:
            raise ValidationError(message_code="INVALID_PASSWORD")
        return result

    @staticmethod
    def validate_name(name: str):
        result = StringValidate.check_no_contains_number(input=name)
        if not result:
            raise ValidationError(message_code="INVALID_NAME")
        return result

    @staticmethod
    def validate_email(email: str):
        result = StringValidate.check_email_format(input=email)
        if not result:
            raise ValidationError(message_code="INVALID_EMAIL")
        return result

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
