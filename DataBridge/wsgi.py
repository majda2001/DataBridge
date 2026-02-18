"""
WSGI config for DataBridge project.

It exposes the WSGI callable as a module-level variable named ``app`` for Vercel.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataBridge.settings')

app = get_wsgi_application()  