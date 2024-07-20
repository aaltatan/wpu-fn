"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from pathlib import Path

from django.core.asgi import get_asgi_application

from blacknoise import BlackNoise
from dotenv import load_dotenv

BASE_DIR = Path().resolve()
load_dotenv(BASE_DIR / '.env')

settings_module: str = 'dev' if os.getenv('DEBUG') == 'TRUE' else 'prod'

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    f"core.settings.{settings_module}"
)

application = BlackNoise(get_asgi_application())
application.add(BASE_DIR / 'static', 'static')