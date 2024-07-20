from .base import *


DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
  'debug_toolbar',
]

MIDDLEWARE += [
  "debug_toolbar.middleware.DebugToolbarMiddleware",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "app.db",
    }
}

STATICFILES_DIRS = [
  BASE_DIR / 'static'
]

INTERNAL_IPS = [
    "127.0.0.1",
]