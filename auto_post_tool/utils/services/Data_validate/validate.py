import re
from django.conf import settings


class CheckValidate:
    def __init__(self, input_string: str):
        self.input_string = input_string

    def check_minimum_length(self):
        match = re.match(settings.REGEX_MINIMUM_LENGTH, self.input_string)
        return bool(match)

    def check_contains_number_and_letter(self):
        match = re.match(settings.REGEX_CONTAIN_NUMBER_AND_LETTER, self.input_string)
        return bool(match)

    def check_no_contains_number(self):
        match = re.search(settings.REGEX_CONTAIN_NO_NUMBER, self.input_string)
        return bool(match)

    def check_email_format(self):
        match = re.match(settings.REGEX_EMAIL, self.input_string)
        return bool(match)
