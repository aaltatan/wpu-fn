from .base import *


DEBUG = True

ALLOWED_HOSTS = []

MIDDLEWARE += [
    "querycount.middleware.QueryCountMiddleware"
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "app.db",
    }
}

STATICFILES_DIRS = [BASE_DIR / "static"]

QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG':0,
        'MIN_QUERY_COUNT_TO_LOG':0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': 1,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}