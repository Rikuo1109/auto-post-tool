"""
    Django settings for Auto post tool project.

    For more information on this file, see
    https://docs.djangoproject.com/en/3.2/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import json
import os
import warnings
from datetime import timedelta
from os.path import dirname, join
from pathlib import Path

from dotenv import load_dotenv


# Ignore warnings
warnings.filterwarnings("ignore")


ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

env_file_name = f"env/{ENVIRONMENT}.env"

dotenv_path = join(dirname(__file__), f"../{env_file_name}")
load_dotenv(dotenv_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PRODUCT_NAME = os.environ.get("PROJECT_NAME", "EB3 Admin")
VERSION = os.environ.get("VERSION", "1.0")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "True"

ALLOWED_HOSTS = json.loads(str(os.environ.get("ALLOWED_HOSTS")))


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # # Third-party apps
    "corsheaders",
    "ninja_extra",
    # local apps
    "user_account",
    "post_management",
    "token_management",
    "image_management",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middleware
    "utils.middleware.ResponseHandleWiddleware",
]

ROOT_URLCONF = "auto_post_tool.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "auto_post_tool.wsgi.application"

# Change user model
AUTH_USER_MODEL = "user_account.User"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE"),
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

# JWT Settings
ACCESS_TOKEN_LIFETIME = int(str(os.environ.get("ACCESS_TOKEN_LIFETIME")))
REFRESH_TOKEN_LIFETIME = int(str(os.environ.get("REFRESH_TOKEN_LIFETIME")))
RESET_PASSWORD_TOKEN_LIFETIME = int(str(os.environ.get("RESET_PASSWORD_TOKEN_LIFETIME")))


NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=REFRESH_TOKEN_LIFETIME),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "email",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# EMAIL CONFIGURATION
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = int(str(os.environ.get("EMAIL_TIMEOUT")))

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE")

TIME_ZONE = os.environ.get("TIME_ZONE")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = bool(os.environ.get("CORS_ALLOW_ALL_ORIGINS"))

# Pagination
DEFAULT_PAGE_SIZE = int(str(os.environ.get("DEFAULT_PAGE_SIZE")))
PAGE_SIZE_MAX = int(str(os.environ.get("PAGE_SIZE_MAX")))

# ADMIN USER
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# UID
BASE_UI_URL = os.environ.get("BASE_UI_URL")
BASE_MEDIA_HOST = os.environ.get("BASE_MEDIA_HOST")

# media directory in the root directory
MEDIA_ROOT = os.path.join(BASE_DIR, str(os.environ.get("MEDIA_ROOT")))
MEDIA_URL = str(os.environ.get("MEDIA_URL"))


NINJA_DOCS_VIEW = "redoc"

# Logging Settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[%(asctime)s] [%(levelname)s] %(message)s", "datefmt": "%d/%b/%Y %H:%M:%S"},
        "color_formatter": {"()": "utils.logging.formatter.Formatter"},  # colored output
    },
    "handlers": {"console_handler": {"class": "logging.StreamHandler", "formatter": "color_formatter"}},
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["console_handler"], "propagate": False, "formatter": "color_formatter"},
        "API": {"level": "DEBUG", "handlers": ["console_handler"], "propagate": False, "formatter": "color_formatter"},
    },
}

# media directory in the root directory
MEDIA_ROOT = os.path.join(BASE_DIR, str(os.environ.get("MEDIA_ROOT")))
MEDIA_URL = str(os.environ.get("MEDIA_URL"))

STATICFILES_DIRS = ("/static/",)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = os.environ.get("STATIC_URL")

JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

JWT_EXPIRED_TIME = int(str(os.environ.get("JWT_EXPIRED_TIME")))

RESET_TOKEN_LENGTH = int(str(os.environ.get("RESET_PASSWORD_TOKEN_LENGTH")))

FACEBOOK_API_APP_ID = os.environ.get("FACEBOOK_API_APP_ID")
FACEBOOK_API_APP_SECRET = os.environ.get("FACEBOOK_API_APP_SECRET")
FACEBOOK_API_VERSION = os.environ.get("FACEBOOK_API_VERSION")
FACEBOOK_LONG_LIVE_TOKEN_LIFETIME = os.environ.get("FACEBOOK_LONG_LIVE_TOKEN_LIFETIME")
FACEBOOK_ACCESS_TOKEN_URL = os.environ.get("FACEBOOK_ACCESS_TOKEN_URL")

ZALO_API_APP_ID = os.environ.get("ZALO_API_APP_ID")
ZALO_API_REQUEST_CONTENT_TYPE = os.environ.get("ZALO_API_REQUEST_CONTENT_TYPE")
ZALO_API_APP_SECRET = os.environ.get("ZALO_API_APP_SECRET")
ZALO_ACCESS_TOKEN_URL = os.environ.get("ZALO_ACCESS_TOKEN_URL")

REQUEST_TIMEOUT = int(str(os.environ.get("REQUEST_TIMEOUT")))


REGEX_MINIMUM_LENGTH = os.environ.get("REGEX_MINIMUM_LENGTH")
REGEX_CONTAIN_NO_NUMBER = os.environ.get("REGEX_CONTAIN_NO_NUMBER")
REGEX_CONTAIN_NUMBER_AND_LETTER = os.environ.get("REGEX_CONTAIN_NUMBER_AND_LETTER")
REGEX_EMAIL = os.environ.get("REGEX_EMAIL")
