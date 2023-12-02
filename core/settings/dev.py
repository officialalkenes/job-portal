from .base import *  # noqa

from decouple import config

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config("NAME"),  # noqa
        # "HOST": config("HOST"),
        "USER": config("USER"),  # noqa
        "PASSWORD": config("PASSWORD"),
    }
}


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa
STATIC_ROOT = "staticfiles"


# COMPRESS_ROOT = BASE_DIR / "static"

# COMPRESS_ENABLED = True

# STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)


# CELERY AND CELERY BEAT
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Lagos"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


# EMAIL SETUP
if DEBUG:  # noqa
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    # EMAIL_PORT = ''
    # EMAIL_HOST_USER = 'your@djangoapp.com'
    # EMAIL_HOST_PASSWORD = 'your-email account-password'
    # EMAIL_USE_TLS = True
    # EMAIL_USE_SSL = False
    # EMAIL_FILE_PATH = "/tmp/messages"  # change this to a proper location

LOGIN_ATTEMPTS_TIME_LIMIT = 18000
MAX_LOGIN_ATTEMPTS = 3

VENV_BASE = os.environ["VIRTUAL_ENV"]  # noqa

# C:\dev\job\venv\Lib\site-packages
GEOS_LIBRARY_PATH = VENV_BASE + "/Lib/site-packages/osgeo/geos_c.dll"
GDAL_LIBRARY_PATH = VENV_BASE + "/Lib/site-packages/osgeo/gdal304.dll"
