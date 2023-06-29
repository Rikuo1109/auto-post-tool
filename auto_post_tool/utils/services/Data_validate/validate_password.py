from django.conf import settings


class PasswordValidate:
    @staticmethod
    def check_minimum_length(password: str):
        return len(password) > int(settings.PASSWORD_MINIMUM_LENGTH)

    @staticmethod
    def check_contains_number(password: str):
        for char in password:
            if char.isdigit():
                return True
        return False
