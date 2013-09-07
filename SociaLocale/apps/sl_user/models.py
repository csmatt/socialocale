import logging
from SociaLocale.apps.interests.models import Interest, InterestFactory
from userena.models import UserenaBaseProfile
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.utils.translation import ugettext as _
from django.contrib.gis.geos import GEOSGeometry
from django.db import models
from annoying.fields import AutoOneToOneField

class UserSettings(models.Model):
    # Map settings
    map_zoom = gis_models.IntegerField(default=15)
    # FB settings
    publish_to_fb = gis_models.BooleanField(default=True)
    notify_on_new_users_with_interest = gis_models.BooleanField(default=True)


class UserProfile(UserenaBaseProfile, gis_models.Model):
    user = gis_models.OneToOneField(User, unique=True,verbose_name=_('user'),related_name='profile')
    interests = gis_models.ManyToManyField(Interest, related_name='+')
    selectedInterest = gis_models.ForeignKey(Interest, related_name='+', null=True, blank=True)
    settings = gis_models.OneToOneField('UserSettings')

    city = gis_models.CharField(max_length=100, null=True) # TODO: change to something like 'locationString'
    location = gis_models.PointField(null=True)
    objects = gis_models.GeoManager()

    def isNewUser(self):
        return self.location == None
        #return (self.interests.count() == 0 or self.selectedInterest == None or self.location == None)

    def save(self, force_insert=False, force_update=False, using=None):
        if self.pk is None:
            self.settings = UserSettings.objects.create()
        self.settings.save()
        super(UserProfile, self).save()

    def setLocation(self, lat, lon, city=None):
        if city:
            self.city = city
        if not self.location:
            self.location = GEOSGeometry('POINT(%s %s)' % (lat, lon))
        else:
            self.location.set_x(float(lat))
            self.location.set_y(float(lon))
        self.save()

# For Tests
import factory


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = "testclient"
    first_name = "Test"
    last_name = "Client"
    is_active = True
    is_superuser = False
    is_staff = False
    last_login = "2006-12-17 07:03:31"
    groups = []
    user_permissions = []
    password = "sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161"
    email = "testclient@example.com"
    date_joined = "2006-12-17 07:03:31"


class UserSettingsFactory(factory.Factory):
    city = "Stuart, FL"
    location = GEOSGeometry('POINT (27.1975480000000012 -80.2528257000000167)')
    map_zoom = 15
    publish_to_fb = True
    notify_on_new_users_with_interest = True


class UserProfileFactory(factory.Factory):
    FACTORY_FOR = UserProfile

    user = factory.SubFactory(UserFactory)

    @classmethod
    def _prepare(cls, create, **kwargs):
        interest1 = InterestFactory(name='interest1')
        userProfile = super(UserProfileFactory, cls)._prepare(create, **kwargs)
        userProfile.interests.add(interest1)
        selectedInterest = interest1
