from django.conf.global_settings import MEDIA_ROOT, MEDIA_URL
import os
import django.conf.global_settings as DEFAULT_SETTINGS
from path import path
import sys

PROJECT_ROOT = path(__file__).abspath().dirname().dirname() # where the project lives
SITE_ROOT = PROJECT_ROOT.dirname() # where manage.py lives
sys.path.append(SITE_ROOT)
sys.path.append(PROJECT_ROOT / 'apps')

ROOT_URLCONF = 'SociaLocale.urls'
SECRET_KEY = '' # add your own

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'south',
    'openid',
    'oauth2',
    'easy_thumbnails',
    'rest_framework',
    'SociaLocale.apps.main',
    'SociaLocale.apps.sl_user',
    'SociaLocale.apps.interests',
    #'SociaLocale.apps.broadcasts',
    'SociaLocale.apps.messages',
    'userena',
    'userena.contrib.umessages',
    'guardian',
    'social_auth',
    'annoying',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

STATICFILES_DIRS = (
    ("static", PROJECT_ROOT+"/apps/main"),
    ("static", PROJECT_ROOT+"/apps/broadcasts"),
    ("static", PROJECT_ROOT+"/apps/interests"),
    ("static", PROJECT_ROOT+"/apps/messages")
)
MEDIA_ROOT = PROJECT_ROOT + "/media"
MEDIA_URL = '/media/'
USERENA_MUGSHOT_GRAVATAR = False
USERENA_MUGSHOT_SIZE = 200
STATIC_ROOT = PROJECT_ROOT + "/static"
STATIC_URL = '/static/'
#STATICFILES_STORAGE = "'django.contrib.staticfiles.storage.StaticFilesStorage'"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)


AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
)

LOGIN_URL          = '/login-form/'
LOGOUT_URL = '/user/signout'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'

## BEGIN USERENA SETTINGS ##
USERENA_USE_HTTPS = False
ANONYMOUS_USER_ID = 1
AUTH_PROFILE_MODULE = 'sl_user.UserProfile'
## END USERENA SETTINGS ##


## BEGIN SOCIAL_AUTH SETTINGS ##
#from django.template.defaultfilters import slugify
SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.process_exceptions'
SOCIAL_AUTH_COMPLETE_URL_NAME='socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME='associate_complete'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
##SOCIAL_AUTH_EXTRA_DATA=False
SOCIAL_AUTH_CHANGE_SIGNAL_ONLY=True
#SOCIAL_AUTH_ASSOCIATE_BY_MAIL=True # associate user via email
SOCIAL_AUTH_LOGIN_REDIRECT_URL='/' #'/accounts/profile/'

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'SociaLocale.apps.sl_user.pipeline.create_profile',
    'SociaLocale.apps.sl_user.pipeline.set_guardian_permissions',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.parsers.JSONParser',
    )
}

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION
