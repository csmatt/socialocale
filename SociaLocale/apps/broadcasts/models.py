from SociaLocale.apps.interests.models import Interest
from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Broadcast(models.Model):
    author = models.ForeignKey(User, null=False, blank=False)
    interest = models.ForeignKey(Interest, null=False, blank=False)
    content = models.TextField()
    when_created = models.DateTimeField(auto_now_add=True)
    location = models.PointField(srid=4326, blank=True, null=True)
    objects = models.GeoManager()

# For Tests
import datetime
import factory
from SociaLocale.apps.sl_user.models import UserProfileFactory
from SociaLocale.apps.interests.models import InterestFactory
class BroadcastFactory(factory.Factory):
    FACTORY_FOR = Broadcast
    author = factory.SubFactory(UserProfileFactory)
    interest = factory.SubFactory(InterestFactory)
    content = 'Broadcast Content'
    when_created = datetime.datetime.now()
