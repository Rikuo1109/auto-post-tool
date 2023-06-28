from .validate import CheckValidate
from utils.exceptions.exceptions import ValidationError


def validate_username(input_string: str):
    result = CheckValidate(input_string).check_minimum_length()
    if not result:
        raise ValidationError(message_code="INVALID_USERNAME")
    return result


def validate_password(input_string: str):
    result = CheckValidate(input_string).check_minimum_length() and CheckValidate(input_string).check_contains_number_and_letter()
    if not result:
        raise ValidationError(message_code="INVALID_PASSWORD")
    return result


def validate_name(input_string: str):
    result = CheckValidate(input_string).check_no_contains_number()
    if not result:
        raise ValidationError(message_code="INVALID_NAME")
    return result


def validate_email(input_string: str):
    result = CheckValidate(input_string).check_email_format()
    if not result:
        raise ValidationError(message_code="INVALID_EMAIL")
    return result


def validate_register(data: dict):
    return (
        validate_name(input_string=data.get("first_name"))
        and validate_password(input_string=data.get("password"))
        and validate_name(input_string=data.get("last_name"))
        and validate_email(input_string=data.get("email"))
        and validate_username(input_string=data.get("username"))
    )


def validate_info(data: dict):
    return (
        validate_name(input_string=data.get("first_name"))
        and validate_name(input_string=data.get("last_name"))
        and validate_username(input_string=data.get("username"))
    )
