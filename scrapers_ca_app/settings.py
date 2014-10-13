"""
Django settings for scrapers_ca_app project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '4y+vddl4y0&h)kl2hmo1iv8_8*s#fta#rt)3-)cel_51ysdu41')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.getenv('PRODUCTION', False)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['scrapers.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'reports',
)

MIDDLEWARE_CLASSES = (
    # @see https://docs.djangoproject.com/en/1.7/ref/middleware/#django.middleware.gzip.GZipMiddleware
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'scrapers_ca_app.urls'

WSGI_APPLICATION = 'scrapers_ca_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


# @see https://devcenter.heroku.com/articles/getting-started-with-django#settings-py
# @see https://devcenter.heroku.com/articles/django-assets

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost/pupa')}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
)

# Error reporting.
ADMINS = (
    ('James McKinney', 'james@opennorth.ca'),
)
# @see https://sendgrid.com/docs/Integrate/Frameworks/django.html
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', None)
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', None)
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Error logging.
# @see https://github.com/etianen/django-herokuapp#outputting-logs-to-heroku-logplex
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'reports': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
