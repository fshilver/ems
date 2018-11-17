from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/home/docker/static/'
MEDIA_ROOT = '/home/docker/media/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ["MYSQL_HOST"].strip(),
        'PORT': os.environ["MYSQL_PORT"].strip(),
        'USER': 'root',
        'PASSWORD': os.environ["MYSQL_ROOT_PASSWORD"].strip(),
        'NAME': os.environ["MYSQL_DATABASE"].strip(),
        'CASE_SENSITIVE' : False,
    }
}
