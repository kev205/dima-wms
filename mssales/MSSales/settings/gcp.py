from .base import *

from urllib.parse import urlparse

GS_BUCKET_NAME = env("GS_BUCKET_NAME")
GS_FILE_OVERWRITE = False
GS_DEFAULT_ACL = "publicRead"
GS_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

# s3 public static settings
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
STATIC_ROOT = None

# s3 public media settings
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
MEDIA_ROOT = None


CLOUDRUN_SERVICE_URLS = env("CLOUDRUN_SERVICE_URLS", default=None)
ADDITIONAL_CLOUDRUN_SERVICE_URLS = env("ADDITIONAL_CLOUDRUN_SERVICE_URLS", default=None)

CSRF_TRUSTED_ORIGINS = []
if CLOUDRUN_SERVICE_URLS:
    CSRF_TRUSTED_ORIGINS = CLOUDRUN_SERVICE_URLS.split(",")
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
if ADDITIONAL_CLOUDRUN_SERVICE_URLS:
    ADDITIONAL_CLOUDRUN_SERVICE_URLS = ADDITIONAL_CLOUDRUN_SERVICE_URLS.split(",")
    CSRF_TRUSTED_ORIGINS += ADDITIONAL_CLOUDRUN_SERVICE_URLS

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

ALLOWED_HOSTS = [urlparse(url).netloc for url in CSRF_TRUSTED_ORIGINS]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {"location": "media"},
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {"location": "staticfiles"},
    },
}

if env("USE_CLOUD_SQL_AUTH_PROXY", default=False):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432
