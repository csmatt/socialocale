from django.conf.urls import *
from SociaLocale.apps.sl_user.views import *

urlpatterns = patterns('',
                       url(r'^details$', MeProfile.as_view()),
                       url(r'^editProfile', UploadProfile.as_view()),
                       url(r'^details/base/(?P<user>\w+)', BasicUserDetails.as_view()),
                       url(r'^details/full/(?P<user>\w+)', FullUserDetails.as_view()),
                       url(r'^settings', SetSettings.as_view()),
                       url(r'^signout', LogoutView.as_view()),
                       url(r'^users', UsernameAutocomplete.as_view())
)