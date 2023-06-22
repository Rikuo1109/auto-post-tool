import re
from utils.exceptions.exceptions import ValidationError

NAME = r"^[^\d]+$"
PASSWORD = r"[a-zA-Z0-9]{8,}$"
EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def validate_name(first_name, last_name):
    if not re.match(NAME, first_name):
        raise ValidationError(message_code="INVALID_FIRST_NAME")
    if not re.match(NAME, last_name):
        raise ValidationError(message_code="INVALID_LAST_NAME")


def validate_password(password):
    if not re.match(PASSWORD, password):
        raise ValidationError(message_code="INVALID_PASSWORD")


def validate_username(username):
    if len(username) < 8:
        raise ValidationError(message_code="INVALID_USERNAME")


def validate_email(email):
    if not re.match(EMAIL, email):
        raise ValidationError(message_code="INVALID_EMAIL")


def validate_register(data:dict):
    # TODO: Tạo regex cho contanst

    try:
        validate_name(data.get("first_name"), data.get("last_name"))
        validate_password(data.get("password"))
        validate_username(data.get("username"))
        validate_email(data.get("email"))
    except NameError:
        raise ValidationError(message_code="DATA_MISSING")


def validate_update_password(data:dict):
    try:
        validate_password(data.get("current_password"))
        validate_password(data.get("new_password"))
    except NameError:
        raise ValidationError(message_code="DATA_MISSING")


def validate_update_info(data:dict):
    try:
        validate_name(data.get("first_name"), data.get("last_name"))
        validate_username(data.get("username"))
    except NameError:
        raise ValidationError(message_code="DATA_MISSING")
