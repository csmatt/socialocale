from django.http import HttpResponse, HttpResponseRedirect
from models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from rest_framework.renderers import JSONPRenderer, JSONRenderer
from serializers import MeProfileSerializer, BasicUserSerializer, BasicUserProfileSerializer, FullUserProfileSerializer
from django.views.generic import View, TemplateView
from django.contrib.gis.geos import GEOSGeometry

class MeProfile(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.isNewUser():
            return Response({'isNewUser': True})
        else:
            serializer = MeProfileSerializer(userProfile)
            return Response(serializer.data)

class BasicUserDetails(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        profile = UserProfile.objects.get(user=request.user)
        serializer = BasicUserProfileSerializer(profile)
        return Response(serializer.data)

class FullUserDetails(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        profile = UserProfile.objects.get(user=request.user)
        serializer = FullUserProfileSerializer(profile)
        return Response(serializer.data)

from forms import EditProfileForm as edit_profile_form
class UploadProfile(View):
    def post(self, request, *args, **kwargs):
        uploaded = request.FILES.get('files[]', None)
        user = request.user
        profile = user.get_profile()

        user_initial = {'first_name': user.first_name,
                        'last_name': user.last_name}

        if request.method == 'POST':
            form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                     initial=user_initial)
            profile = form.save()
            locationParam = request.POST.get('location')
            if locationParam and ';' in locationParam:
                lat, lon = locationParam.split(';')
                profile.setLocation(lat, lon)
        return HttpResponse()

class SetSettings(APIView):
    def post(self, request, *args, **kwargs):
        location = {}
        userProfile = UserProfile.objects.get(user=request.user)
        for key, value in request.POST.iteritems():
            if key == 'location[lat]' or key == 'location[lon]':
                if key == 'location[lat]':
                    location['lat'] = value
                if key == 'location[lon]':
                    location['lon'] = value
                if location.has_key('lat') and location.has_key('lon'):
                    userProfile.setLocation(location['lat'], location['lon'])
            elif key == 'map_zoom':
                userProfile.settings.map_zoom = value
        userProfile.save()
        return Response()

class UsernameAutocomplete(APIView):
    def get(self, request, *args, **kwargs):
        queryStr = request.GET.get('q')
        if len(queryStr) < 2:
            return Response()
        users = User.objects.filter(username__startswith=queryStr).distinct('username')
        serializer = BasicUserSerializer(users, many=True)
        return Response(serializer.data)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        """Logs out user"""
        auth_logout(request)
        return HttpResponseRedirect('/')