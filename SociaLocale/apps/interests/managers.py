from SociaLocale.apps.interests.models import Interest
import json
from urllib import unquote
import urllib2, logging

def getFacebookLike(interest_id):
    # TODO: possibly unsafe
    BASE_FB_URL = "https://graph.facebook.com/"
    obj = json.loads(urllib2.urlopen(url=BASE_FB_URL + interest_id).read())
    if not isinstance(obj, dict):
        raise Exception("No object returned from facebook for id: %s" % interest_id)
    obj['picture'] = "%s/%s/picture" % (BASE_FB_URL, interest_id)
    return obj

def create(fb_id):
    if Interest.objects.filter(fb_id=fb_id).exists():
        return Interest.objects.get(fb_id=fb_id)
    else:
        obj = getFacebookLike(fb_id)
        interest = Interest(name=obj['name'], category=obj['category'], picture=obj['picture'], fb_id=fb_id)
        interest.save()
        return interest
