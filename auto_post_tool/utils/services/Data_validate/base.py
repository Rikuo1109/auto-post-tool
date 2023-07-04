import re

CONTAIN_NUMBER = "^(?=.*\d).+$"
EMAIL = "^[\w+\.-]+@[\w+\.-]+\.\w+$"
NOT_CONTAIN_SPACE = "^(?=.*\s).+$"


class BaseValidator(object):
    @staticmethod
    def is_longer_than(value: str, max_length: int) -> bool:
        return bool(len(value) >= max_length)

    @staticmethod
    def is_contain_number(value: str) -> bool:
        return bool(re.match(CONTAIN_NUMBER, value))

    @staticmethod
    def check_email_format(value: str):
        return bool(re.match(EMAIL, value))

    @staticmethod
    def is_contain_space(value: str):
        return bool(re.match(NOT_CONTAIN_SPACE, value))
