from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()
env.smart_cast = False

DEBUG = False
SECRET_KEY = (
    "django-insecure-n=e%k)a(l_=vqwxdyx5f#oc87addn7r-$q)!8amx2eswkrgx18"
)

TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = "ru-RU"
USE_I18N = True
USE_TZ = True
env.read_env(str(BASE_DIR / ".env"))


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
EMAIL_SUBJECT_PREFIX = '[HelpDesk]'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": 5432,
        "ATOMIC_REQUESTS": True,
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
#     }
# }


AUTH_USER_MODEL = 'requesting.CustomUser'


JAZZMIN_SETTINGS = {
    "site_title": "Админ панель",
    "site_brand": "Админ панель",
    "copyright": "",
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "main.urls"
ASGI_APPLICATION = "main.asgi.application"
STATIC_ROOT = BASE_DIR / "staticfiles"

INSTALLED_APPS = [
    'jazzmin',
    "requesting",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "crispy_bootstrap5",
    "crispy_forms",
    "dashboard",
    "imagekit",
]


LOGIN_REDIRECT_URL = "new"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = LOGIN_URL

_PASS = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{_PASS}.UserAttributeSimilarityValidator"},
    {"NAME": f"{_PASS}.MinimumLengthValidator"},
    {"NAME": f"{_PASS}.CommonPasswordValidator"},
    {"NAME": f"{_PASS}.NumericPasswordValidator"},
    # {"NAME": "requesting.password_validation.PasswordValidator"},
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_URL = "static/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"
# STATICFILES_DIRS = [BASE_DIR / "static"]
ALLOWED_HOSTS = ["*"]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}
