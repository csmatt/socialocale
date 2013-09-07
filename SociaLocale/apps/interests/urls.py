from django.conf.urls import *
from views import *

urlpatterns = patterns('',
                       url(r'^add', AddInterest.as_view()),
                       url(r'^delete', DeleteInterest.as_view()),
                       url(r'^selected', SelectedInterest.as_view()),
                       url(r'', ListInterests.as_view()),
                       )