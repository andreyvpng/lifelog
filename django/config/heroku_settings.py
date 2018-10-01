from config.common_settings import *
import django_heroku

INSTALLED_APPS = INSTALLED_APPS + [
    'raven.contrib.django.raven_compat',
]

django_heroku.settings(locals())
