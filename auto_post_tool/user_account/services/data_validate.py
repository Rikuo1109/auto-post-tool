import re
from django.core.exceptions import ValidationError


def validate(data: dict):
    # Validate first name
    if not re.match(r"^[^\d]+$", data.first_name):
        raise ValidationError("Invalid Firstname")
    # Validate last name
    if not re.match(r"^[^\d]+$", data.last_name):
        raise ValidationError("Invalid Lastname")
    # Validate password (at least 8 characters, starts with uppercase, contains number)
    if not re.match(r"[a-zA-Z0-9]{8,}$", data.password):
        raise ValidationError(
            "Invalid Password"
        )
    # Validate username (at least 8 characters)
    if len(data.username) < 8:
        raise ValidationError("Invalid Username")
    # Validate email format
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", data.email):
        raise ValidationError("Invalid email format")
    else:
        return data
    
def validate_password(password: str):
    if not re.match(r"[a-zA-Z0-9]{8,}$", password):
        raise ValidationError(
            "Invalid Password"
        )

def validate_info(data:dict):
    if not re.match(r"^[^\d]+$", data.first_name):
        raise ValidationError("Invalid Firstname")

    if not re.match(r"^[^\d]+$", data.last_name):
        raise ValidationError("Invalid Lastname")

    if len(data.username) < 8:
        raise ValidationError("Invalid Username")