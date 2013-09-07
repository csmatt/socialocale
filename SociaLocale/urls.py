# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf.urls import *
from django.views.decorators.csrf import ensure_csrf_cookie
from SociaLocale.apps.main.views import Root, LandingPage
urlpatterns = patterns('',
    url(r'^interests/', include('SociaLocale.apps.interests.urls')),
    url(r'^user/', include('SociaLocale.apps.sl_user.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^messages/', include('SociaLocale.apps.messages.urls')),
    url('^landing', ensure_csrf_cookie(LandingPage.as_view())),
    url('^$', ensure_csrf_cookie(Root.as_view())),
    url('^subscribe/', LandingPage.as_view()),
    url(r'', include('social_auth.urls')),

    #Route('/privacy', handler='controllers.handlers.PrivacyPolicyHandler'),
    #Route('/og/interest', OpenGraphHandler),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
from settings import common
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
# Add media and static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(common.MEDIA_URL, document_root=common.MEDIA_ROOT)