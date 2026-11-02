"""Expose the Django WSGI application to Vercel's Python runtime."""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cems.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
