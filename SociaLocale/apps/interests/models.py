from django.db import models

class Interest(models.Model):
    name = models.CharField(max_length=50, blank=False) # TODO: required
    category = models.CharField(max_length=50) # TODO: required
    picture = models.CharField(max_length=100)
    fb_id = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

# For Tests
import factory
class InterestFactory(factory.Factory):
    FACTORY_FOR = Interest
    name = 'InterestName'
    category = 'Category'
    picture = 'http://www.socialocale.com/picture'
    fb_id = 1
