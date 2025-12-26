from .base import *

import os
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('TEST_DB_NAME', default='geo_points_test_db'),
        'USER': config('TEST_DB_USER', default='postgres'),
        'PASSWORD': config('TEST_DB_PASSWORD', default='Ser19052001'),
        'HOST': config('TEST_DB_HOST', default='localhost'),
        'PORT': config('TEST_DB_PORT', default='5432'),
    }
}

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-development-key-change-me-in-production!')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}