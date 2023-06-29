from django.conf import settings


class UsernameValidate:
    @staticmethod
    def check_minimum_length(username: str):
        return len(username) > int(settings.USERNAME_MINIMUM_LENGTH)
