"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django.test as django_test
from models import UserProfileFactory

class SociaLocaleTestCase(django_test.TestCase):
    def test_basic_view(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        def test_users_with_same_interest_and_location_are_returned(self):
            user1 = UserProfileFactory()
            user2 = UserProfileFactory()
            c = django_test.client.Client()
            data = {
                'neMapBounds': '27.208292,-80.230853',
                'swMapBounds': '27.186803,-80.274798',
                'mapCenterLat': '27.197548',
                'mapCenterLon': '-80.25282570000002',
            }
            response = c.get("/listUsersAndBroadcastsForInterest/", data)
            print response
            #self.assertContains(response, )

