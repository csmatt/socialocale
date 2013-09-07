# Copy this file into secrets.py and set keys, secrets and scopes.
import os
# This is a session secret key used by webapp2 framework.
# Get 'a random and long string' from here: 
# http://clsc.net/tools/random-string-generator.php
# or execute this from a python shell: import os; os.urandom(64)
SESSION_KEY = ""

# add your own for each
AUTH_INFO = {
    'GOOGLE_OAUTH2_CLIENT_ID': ['','']
    'GOOGLE_OAUTH2_CLIENT_SECRET': ['', '']

    'FACEBOOK_APP_ID': ['', '']
    'FACEBOOK_API_SECRET': ['', '']
    'FACEBOOK_CANVAS_NAME': ['' '']
    'FACEBOOK_APP_URI': ['', '']

    'LINKEDIN_CONSUMER_KEY': ['', '']
    'LINKEDIN_CONSUMER_SECRET': ['', '']

    'WL_CLIENT_ID': ['', '']
    'WL_CLIENT_SECRET': ['', '']

    'TWITTER_CONSUMER_KEY': ['', '']
    'TWITTER_CONSUMER_SECRET': ['', '']
}

# TEST = 0
# LIVE = 1
# VERSION = TEST
# SITES = ['http://localhost:8000/', 'http://www.socialocale.com/']
#
# # The App's base URL
# SITE = SITES[VERSION]
#
# # Google APIs
# GOOGLE_APP_ID = AUTH_INFO['GOOGLE_APP_ID'][VERSION]
# GOOGLE_APP_SECRET = AUTH_INFO['GOOGLE_APP_SECRET'][VERSION]
#
# # Facebook auth apis
# FACEBOOK_APP_ID = AUTH_INFO['FACEBOOK_APP_ID'][VERSION]
# FACEBOOK_APP_SECRET = AUTH_INFO['FACEBOOK_APP_SECRET'][VERSION]
# FACEBOOK_CANVAS_NAME = AUTH_INFO['FACEBOOK_CANVAS_NAME'][VERSION]
# FACEBOOK_APP_URI = AUTH_INFO['FACEBOOK_APP_URI'][VERSION]
#
# # https://www.linkedin.com/secure/developer
# LINKEDIN_CONSUMER_KEY = AUTH_INFO['LINKEDIN_CONSUMER_KEY'][LIVE]
# LINKEDIN_CONSUMER_SECRET = AUTH_INFO['LINKEDIN_CONSUMER_SECRET'][LIVE]
#
# # https://manage.dev.live.com/AddApplication.aspx
# # https://manage.dev.live.com/Applications/Index
# WL_CLIENT_ID = AUTH_INFO['WL_CLIENT_ID'][LIVE]
# WL_CLIENT_SECRET = AUTH_INFO['WL_CLIENT_SECRET'][LIVE]
#
# # https://dev.twitter.com/apps
# TWITTER_CONSUMER_KEY = AUTH_INFO['TWITTER_CONSUMER_KEY'][LIVE]
# TWITTER_CONSUMER_SECRET = AUTH_INFO['TWITTER_CONSUMER_SECRET'][LIVE]

# config that summarizes the above
"""AUTH_CONFIG = {
  'google'      : (GOOGLE_APP_ID,         GOOGLE_APP_SECRET,        'https://www.googleapis.com/auth/userinfo.profile'),
  'facebook'    : (FACEBOOK_APP_ID,       FACEBOOK_APP_SECRET,      'user_about_me,user_likes,user_interests,user_location'),
  'windows_live': (WL_CLIENT_ID,          WL_CLIENT_SECRET,         'wl.signin'),
  'twitter'     : (TWITTER_CONSUMER_KEY,  TWITTER_CONSUMER_SECRET),
  'linkedin'    : (LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET),
}"""
