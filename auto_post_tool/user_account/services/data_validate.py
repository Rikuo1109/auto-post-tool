import re

from django.core.exceptions import ValidationError


# TODO: Data này kiểu gì???


def validate(data: dict):
    # TODO: Tạo regex cho contanst

    try:
        if not re.match(r"^[^\d]+$", data.first_name):
            raise ValidationError("Invalid Firstname")
        if not re.match(r"^[^\d]+$", data.last_name):
            raise ValidationError("Invalid Lastname")
        if not re.match(r"[a-zA-Z0-9]{8,}$", data.password):
            raise ValidationError("Invalid Password")
        if len(data.username) < 8:
            raise ValidationError("Invalid Username")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", data.email):
            raise ValidationError("Invalid email format")
    except KeyError:
        raise ValidationError("Missing key in data input")


def validate_password(data: dict):
    try:
        if not re.match(r"[a-zA-Z0-9]{8,}$", data.current_password):
            raise ValidationError("Invalid Password")
        if not re.match(r"[a-zA-Z0-9]{8,}$", data.new_pasword):
            raise ValidationError("Invalid Password")
    except KeyError:
        raise ValidationError("Missing key in data input")


def validate_info(data: dict):
    try:
        if not re.match(r"^[^\d]+$", data.first_name):
            raise ValidationError("Invalid Firstname")
        if not re.match(r"^[^\d]+$", data.last_name):
            raise ValidationError("Invalid Lastname")
        if len(data.username) < 8:
            raise ValidationError("Invalid Username")
    except KeyError:
        raise ValidationError("Missing key in data input")
