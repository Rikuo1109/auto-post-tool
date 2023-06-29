import re

EMAIL = "^[\w+\.-]+@[\w+\.-]+\.\w+$"


class EmailValidate:
    @staticmethod
    def check_email_format(email: str):
        return bool(re.match(EMAIL, email))
