"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import redis
from corsheaders.defaults import default_headers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = default_headers + (
    "access-control-allow-headers",
    "access-control-allow-methods",
    "access-control-allow-origin",
)

# Application definition

DJANGO_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "apps.accounts",
    "apps.core",
    "apps.banking",
    "apps.hn",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "social_django",
    "graphene_django",
]

# GraphQL

GRAPHENE = {
    "SCHEMA": "backend.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware"
    ],
}

# Python Social Auth

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

AUTHENTICATION_BACKENDS = (
    "graphql_jwt.backends.JSONWebTokenBackend",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

for key in [
    "GITHUB_KEY",
    "GITHUB_SECRET",
    "GOOGLE_OAUTH2_KEY",
    "GOOGLE_OAUTH2_SECRET",
    "FACEBOOK_KEY",
    "FACEBOOK_SECRET",
]:
    # Use exec instead of eval here because we're not
    # just trying to evaluate a dynamic value here;
    # we're setting a module attribute whose name varies.
    exec(f"SOCIAL_AUTH_{key} = os.environ.get('{key}')")

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    # 'social_core.pipeline.user.get_username',
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# this is needed to get a user's email from Facebook. See:
# https://stackoverflow.com/questions/32024327/facebook-doesnt-return-email-python-social-auth
# https://stackoverflow.com/a/32129851/6084948
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields": "id,name,email",
}

# SOCIAL_AUTH_GITHUB_WHITELISTED_DOMAINS=['localhost']

INSTALLED_APPS = (
    DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),
        "USER": os.environ.get(
            "POSTGRES_USERNAME", "postgres"
        ),
        "PASSWORD": os.environ.get(
            "POSTGRES_PASSWORD", "postgres"
        ),
        "HOST": os.environ.get(
            "POSTGRES_SERVICE_HOST", "postgres"
        ),
        "PORT": os.environ.get(
            "POSTGRES_SERVICE_PORT", 5432
        ),
    }
}

ASGI_APPLICATION = "backend.routing.application"

# Redis

REDIS_SERVICE_HOST = os.environ.get(
    "REDIS_SERVICE_HOST", "redis"
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_SERVICE_HOST, 6379)],  # noqa
        },
    },
}

REDIS = redis.Redis(
    host=REDIS_SERVICE_HOST,
    port=6379,
    db=3,
    charset="utf-8",
    decode_responses=True,
)

# REST FRAMEWORK

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",  # noqa
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}

# Celery Configuration
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


AUTH_USER_MODEL = "accounts.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

AWS_DEFAULT_ACL = None

AWS_STORAGE_BUCKET_NAME = os.environ.get(
    "AWS_STORAGE_BUCKET_NAME", "bucketname"
)
AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_PRIVATE_MEDIA_LOCATION = "media/private"
AWS_STATIC_LOCATION = "static"

PRIVATE_FILE_STORAGE = (
    "backend.storage_backends.PrivateMediaStorage"
)


# Email

EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "mailhog")
EMAIL_PORT = os.environ.get("DJANGO_EMAIL_PORT", "1025")
