import logging
import traceback
from models import Interest
from SociaLocale.apps.sl_user import managers as sl_user_managers
from SociaLocale.apps.sl_user.models import UserProfile
from rest_framework.views import APIView
from rest_framework.renderers import JSONPRenderer, JSONRenderer
from rest_framework.response import Response
from serializers import InterestSerializer
from django.contrib.gis.geos import Polygon
from SociaLocale.apps.sl_user.serializers import BasicUserProfileSerializer

class ListInterests(APIView):
    '''returns the logged in users interests'''
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        interests = UserProfile.objects.get(user=request.user).interests.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data)


class SelectedInterest(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        response = None
        neMapBounds = request.GET.get('neMapBounds')
        swMapBounds = request.GET.get('swMapBounds')
        userProfile = UserProfile.objects.get(user=request.user)
        interest = userProfile.selectedInterest
        if interest:
            (neMapBoundsLat, neMapBoundsLon) = (float(v) for v in neMapBounds.split(','))
            (swMapBoundsLat, swMapBoundsLon) = (float(v) for v in swMapBounds.split(','))
            geom = Polygon.from_bbox((swMapBoundsLat, swMapBoundsLon, neMapBoundsLat, neMapBoundsLon))
            userProfiles = UserProfile.objects.filter(location__within=geom, interests__in=[interest]).exclude(user=request.user)
            interestSerializer = InterestSerializer(interest)
            usersSerializer = BasicUserProfileSerializer(userProfiles, many=True)
            interestSerializer.data['users'] = usersSerializer.data
            response = interestSerializer.data

        return Response(response)

    def post(self, request, interest_id=None, format='json'):
        userProfile = UserProfile.objects.get(user=request.user)
        if not interest_id:
            interest_id = request.POST.get('interest[id]')
        interest = Interest.objects.get(pk=interest_id)
        userProfile.selectedInterest = interest
        userProfile.save()
        return Response()

class AddInterest(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def post(self, request, format='json'):
        try:
            fb_interest_id = self.request.POST.get('interest_id')
            userProfile = sl_user_managers.getUserProfile(self.request)
            interest = sl_user_managers.add_or_update_interest(userProfile, fb_interest_id)
            """if userProfile and userProfile.publish_to_fb:
                try:
                    objType = 'interest'
                    objUrl = '/og/' + objType + '?id=' + str(interest_id)
                    self.facebook.openGraph('add', objType, objUrl)
                except FacebookApiError, e:
                    logging.error(str(e))"""

            return SelectedInterest.as_view()(self.request, interest_id=interest.id)
        except Exception, e:
            # TODO: error feedback
            logging.error(traceback.format_exc())

class DeleteInterest(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def post(self, request, format='json'):
        userProfile = UserProfile.objects.get(user=request.user)
        interest_id = request.POST.get('id')
        interest = Interest.objects.get(pk=interest_id)
        userProfile.interests.remove(interest)
        if interest == userProfile.selectedInterest:
            userInterestList = list(userProfile.interests.all())
            if len(list(userInterestList)) > 0:
                userProfile.selectedInterest = userInterestList[0]
        userProfile.save()
        return Response()


#import conf
#class OpenGraphHandler(webapp2.RequestHandler):
#
#    def get(self):
#        logging.error(self.request.url)
#        interest_id = self.request.get('id')
#        interest = Interest.get_by_key_name(interest_id)
#        #interest_name = urllib.unquote(interest_name.encode('ascii')).decode('utf-8')
#        pictureUrl = "https://graph.facebook.com/%s/picture" % interest.interest_id
#        self.response.headers['Content-Type'] = 'text/html'
#        data = {'conf': conf, 'url': self.request.url, 'name': interest.name, 'picture': pictureUrl}
#        self.response.out.write(render_to_string('./og/interest.html', data))
#
#    def post(self):
#        pass

