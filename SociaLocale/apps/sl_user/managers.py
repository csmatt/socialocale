from models import UserProfile
import logging
from SociaLocale.apps import interests
from SociaLocale.apps.interests import managers as interests_managers

def create_interests(me):
    interests = []
    for key in [u'interests']:
        if key in me:
            for interestObj in me[key][u'data']:
                interest_id = interestObj['id']
                try:
                    add_interest(interest_id)
                except Exception, e:
                    logging.error(e)

def add_interest(userProfile, interest_id):
    interest = interests_managers.create(interest_id)
    if userProfile and (not interest.id in userProfile.interests.all()):
        userProfile.interests.add(interest.id)
    return interest

def add_or_update_interest(userProfile, interest_id):
    interest = add_interest(userProfile, interest_id)
    if userProfile:
        update_recent_interests(userProfile, interest)
        userProfile.selectedInterest = interest
        userProfile.save()
    return interest

def update_recent_interests(userProfile, interest):
    # TODO: fix this
    ##index = userProfile.interests.index(interest.id)
    ##userProfile.interests.pop(index)
    ##userProfile.interests.insert(0, interest.id)
    pass


def getUserProfile(request):
    '''returns the UserProfile object associated with request.user.id if the user is authenticated'''
    if request.user and request.user.is_authenticated():
        userProfile = UserProfile.objects.filter(user=request.user)
        if UserProfile.objects.filter(user=request.user).exists():
            return UserProfile.objects.get(user=request.user)
        else:
            '''if a UserProfile does not exist, but the user is authenticated, create a UserProfile for the current user'''
            userProfile = UserProfile(user=request.user)
            userProfile.setLocation(0,0)
            userProfile.save()
            return userProfile
    else:
        return None