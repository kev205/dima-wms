from .base import *


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="mssales"),
        "USER": env("DB_USER", default="dima"),
        "PASSWORD": env("DB_PASSWORD", default="dima"),
        "HOST": env("DB_HOST", default="db"),
        "PORT": env("DB_PORT", default="5432"),
    },
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


USE_X_FORWARDED_PORT = env("USE_X_FORWARDED_PORT", default=False)