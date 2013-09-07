from common import *
from SociaLocale import secrets

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SITE = 'http://www.socialocale.com/'
SESSION_KEY = secrets.SESSION_KEY
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geodjango',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'PASSWORD': '', # add your own
        'USER': 'postgres'
    }
}
## START SOCIAL_AUTH SETTINGS ##
# Google APIs
GOOGLE_OAUTH2_CLIENT_ID = secrets.AUTH_INFO['GOOGLE_OAUTH2_CLIENT_ID'][DEBUG]
GOOGLE_OAUTH2_CLIENT_SECRET = secrets.AUTH_INFO['GOOGLE_OAUTH2_CLIENT_SECRET'][DEBUG]

# Facebook auth apis
FACEBOOK_APP_ID = secrets.AUTH_INFO['FACEBOOK_APP_ID'][DEBUG]
FACEBOOK_API_SECRET = secrets.AUTH_INFO['FACEBOOK_API_SECRET'][DEBUG]

# https://dev.twitter.com/apps
TWITTER_CONSUMER_KEY = secrets.AUTH_INFO['TWITTER_CONSUMER_KEY'][DEBUG]
TWITTER_CONSUMER_SECRET = secrets.AUTH_INFO['TWITTER_CONSUMER_SECRET'][DEBUG]

SOCIAL_AUTH_RAISE_EXCEPTIONS = DEBUG
## END SOCIAL_AUTH SETTINGS ##
