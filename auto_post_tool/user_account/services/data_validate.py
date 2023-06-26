import re
from utils.exceptions.exceptions import ValidationError
from django.conf import settings

NAME = settings.NAME
PASSWORD = settings.PASSWORD
EMAIL = settings.EMAIL


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


def validate_register(data: dict):
    validate_name(data.get("first_name"), data.get("last_name"))
    validate_password(password=data.get("password"))
    validate_username(username=data.get("username"))
    validate_email(email=data.get("email"))


def validate_update_password(data: dict):
    validate_password(password=data.get("new_password"))


def validate_update_info(data: dict):
    validate_name(first_name=data.get("first_name"), last_name=data.get("last_name"))
    validate_username(username=data.get("username"))
