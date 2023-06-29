import re
from django.conf import settings


class StringValidate:
    @staticmethod
    def check_minimum_length(input: str):
        return len(input) > settings.MINIMUM_LENGTH

    @staticmethod
    def check_contains_number_and_letter(input: str):
        return bool(re.match(settings.CONTAIN_NUMBER_AND_LETTER, input))

    @staticmethod
    def check_no_contains_number(input: str):
        return bool(re.search(settings.CONTAIN_NO_NUMBER, input))

    @staticmethod
    def check_email_format(input: str):
        return bool(re.match(settings.EMAIL, input))
