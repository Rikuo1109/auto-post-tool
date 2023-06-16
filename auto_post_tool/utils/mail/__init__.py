from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .payload import EmailPayload
from .utils import EmailThread


EMAIL_USE_TLS = settings.EMAIL_USE_TLS
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_TIMEOUT = settings.EMAIL_TIMEOUT


class MailSenderService:
    """[Service] - Email sender service

    Params:
    - recipients: required - list of recipients's email / user: User
    - context: optional - dict of context for loading in params
    """

    def __init__(self, recipients, **kwargs):
        self.recipients = recipients

        self.context = kwargs

        self.sender = EMAIL_HOST_USER
        self.port_number = EMAIL_PORT
        self.timeout = EMAIL_TIMEOUT
        self.use_tls = EMAIL_USE_TLS
        self.password = EMAIL_HOST_PASSWORD
        self.provider = EMAIL_HOST