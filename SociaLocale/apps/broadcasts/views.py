from django.shortcuts import render_to_response
from SociaLocale.apps.interests.models import Interest
from models import Broadcast
from SociaLocale.apps.main import managers as socialocale_managers
from SociaLocale.apps.sl_user.models import UserProfile
import json, logging, traceback
from SociaLocale import utilities
#from geomodel.utils import geotypes
from django.contrib.auth.models import User
from SociaLocale.utilities import return_response
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Polygon

def get_broadcasts_for_interest_and_location(request, interest, neMapBoundsLat, neMapBoundsLon, swMapBoundsLat, swMapBoundsLon):
    geom = Polygon.from_bbox((swMapBoundsLat, swMapBoundsLon, neMapBoundsLat, neMapBoundsLon))
    matchingBroadcasts = Broadcast.objects.filter(location__within=geom, interest=interest)
    matchingBroadcastDicts = []
    for matchingBroadcast in matchingBroadcasts:
        matchingBroadcastDicts.append({
            'broadcast_id':str(matchingBroadcast.id),
            'author':{
                'name':matchingBroadcast.author.username,
                'id':matchingBroadcast.author.id,
                #'picture':author.avatar_url
            },
            'content':matchingBroadcast.content,
            'latitude':matchingBroadcast.location.x,
            'longitude': matchingBroadcast.location.y,
            'created': utilities.prettydate(matchingBroadcast.when_created)})
    return matchingBroadcastDicts

#@ajax_request
#def list_users_and_broadcasts_for_map_bounds(request):
#    '''params: neMapBounds[neMapBoundsLat,neMapBoundsLon], swMapBounds[swMapBoundsLat,swMapBoundsLon], mapCenterLat, mapCenterLon, interest_id'''
#    returnObj = {}
#    interest_id = request.GET.get('interest_id')
#    if interest_id:
#        mapCenterLat = request.GET.get('mapCenterLat')
#        mapCenterLon = request.GET.get('mapCenterLon')
#        (neMapBoundsLat, neMapBoundsLon) = (float(v) for v in request.GET.get('neMapBounds').split(','))
#        (swMapBoundsLat, swMapBoundsLon) = (float(v) for v in request.GET.get('swMapBounds').split(','))
#        interest = Interest.objects.get(pk=interest_id)
#        if interest:
#            # TODO: move this block to its own post in the user controller
#            if request.user.is_authenticated():
#                userProfile = managers.getUserProfile(request)
#                userProfile.selectedInterest = interest
#                userProfile.save()
#            matchingUserDicts = get_users_for_interest_and_location(request, interest, neMapBoundsLat, neMapBoundsLon, swMapBoundsLat, swMapBoundsLon)
#            matchingBroadcastDicts = get_broadcasts_for_interest_and_location(request, interest, neMapBoundsLat, neMapBoundsLon, swMapBoundsLat, swMapBoundsLon)
#            returnObj = {
#                'interest_name':utilities.unescape(interest.name),
#                'interest_id':interest_id,
#                'matchingUserDicts':matchingUserDicts,
#                'matchingBroadcastDicts':matchingBroadcastDicts,
#                'latitude': mapCenterLat,
#                'longitude': mapCenterLon
#            }
#        return returnObj
#    """else:
#        location = userProfile.location
#        results = userProfile.proximity_fetch(userProfile.all(), location, max_results=10, max_distance=80467)
#        self.render('map', {'centerMap':location})"""


@return_response
def handle_request(request, action):
        try:
            request_map[request.method][action](request)
        except:
            logging.error(traceback.format_exc())

@login_required
def add(request):
    msgText = request.POST.get('text')
    interest_id = request.POST.get('interest_id')
    interest = Interest.objects.get(pk=interest_id)
    userProfile = socialocale_managers.getUserProfile(request)
    msg = Broadcast(content=msgText, interest=interest, author=request.user, location=userProfile.location)
    msg.save()

@login_required
def delete(request):
    broadcast_id = request.POST.get('broadcast_id')
    broadcast = Broadcast.objects.get(pk=broadcast_id)
    if broadcast.author == request.user:
        broadcast.delete()

def list(request):
    # TODO: use this method or get rid of it
    interest_id = request.GET.get('interest_id')
    interest = Interest.objects.get(pk=interest_id)
    location = socialocale_managers.getUserProfile().location
    # TODO: convert proximity fetch query to GeoDjango
    results = Broadcast.proximity_fetch(Broadcast.objects.all().filter('interest =', interest), location, max_results=10, max_distance=80467)
    broadcasts = []
    for result in results:
        broadcasts.append({'author':result.author.name, 'content':result.content, 'created':result.when_created})
    render_to_response(json.dumps(broadcasts))


request_map = {'GET':
                   {'list': list},
               'POST':
                   {'add': add, 'delete': delete}
}
