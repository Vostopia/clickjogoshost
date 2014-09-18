# Django settings for clickjogoshost project.
import os
import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))

CLICKJOGOS_URL = os.environ.get("CLICKJOGOS_URL", "") or "http://connect.clickjogos.uol.com.br"
CLICKJOGOS_KEY = os.environ["CLICKJOGOS_KEY"]
CLICKJOGOS_SECRET = os.environ["CLICKJOGOS_SECRET"]

GOOGLE_ANALYTICS_PROPERTY = os.environ.get("GOOGLE_ANALYTICS_PROPERTY", "")

ADMINS = (
    ('KvanteTore', 'tore@vostopia.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost/clickjogoshost')
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

#use S3 for static/media files
USE_S3_STORAGE = True
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "") or "vostopia-clickjogos-avatars"
AWS_PRELOAD_METADATA = True

STORAGE_BUCKET_PREFIX = os.environ.get("AWS_STORAGE_BUCKET_PREFIX", "") or "develop"
S3DIRECT_DIR = STORAGE_BUCKET_PREFIX

AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'x-amz-acl': 'public-read',
    'Cache-Control': 'public, max-age=31556926'
}

DEFAULT_FILE_STORAGE = 'apps.storage.storage.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'apps.storage.storage.StaticRootS3BotoStorage'

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + "/" + STORAGE_BUCKET_PREFIX + '/static/'
MEDIA_URL = S3_URL + "/" + STORAGE_BUCKET_PREFIX + '/media/'

#CDN_SERVERS = {}

#CJ Staging CDN
CDN_SERVERS = {
    "http://vostopia-clickjogos-avatars.s3.amazonaws.com/": [
        "http://vostopia.clickjogos.com.br/",
    ],
    "https://vostopia-clickjogos-avatars.s3.amazonaws.com/": [
        "http://vostopia.clickjogos.com.br/",
    ],
}


#use REDIS for sessions if available
REDIS_URL = os.environ.get("REDISCLOUD_URL", "")
if REDIS_URL:
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS_URL = REDIS_URL

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "") or 'dfdfjhytytltlggg9g9ffk4^&&*dlf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'clickjogoshost.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'clickjogoshost.wsgi.application'


AUTH_USER_MODEL = "clickjogosauth.User"
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.clickjogosauth.backends.ClickJogosBackend',
)

INSTALLED_APPS = (
    #built in apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #bootstrap plugin must be before admin
    'django_admin_bootstrapped',

    #admin
    'django.contrib.admin',
    'django.contrib.admindocs',

    #3rd party apps
    'south',
    'gunicorn',

    #project apps
    'apps.clickjogosauth',
    'apps.webplayer',
    'apps.gevent_runserver',
    'apps.storage',

    #external apps copied into project
    'apps.s3direct',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',

            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
