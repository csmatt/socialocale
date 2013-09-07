import re, json, urllib2
from htmlentitydefs import name2codepoint
from functools import wraps
from django.http import HttpResponse

def return_response(fn):
    """Decorator that will return an empty HttpResponse object if the function it decorates returns nothing"""
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        response = fn(request, *args, **kwargs)
        if not response:
            return HttpResponse()
        else:
            return response
    return wrapper

def user_required(fn):
    """Decorator to ensure a user is present"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        handler = args[0]
        if handler.logged_in:
            return fn(*args, **kwargs)
        handler.redirect(u'/')
    return wrapper

def getGeoPtFromAddress(address):
    if not address:
        raise Exception(u'Please specify a location.')
    address = urllib2.quote(address)
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=false'
    result = urllib2.urlopen(url).read()
    geojson = json.loads(result)['results'][0]['geometry']['location']
    lat = geojson['lat']
    lng = geojson['lng']
    ##geoPt = GeoPt(lat, lng)
    ##return geoPt

import datetime
def prettydate(d):
    diff = datetime.datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '%s days ago' % diff.days
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '%s seconds ago' % s
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '%s minutes ago' % (s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '%s hours ago' % (s/3600)

# for some reason, python 2.5.2 doesn't have this one (apostrophe)
name2codepoint['#39'] = 39

def unescape(s):
    "unescape HTML code refs; c.f. http://wiki.python.org/moin/EscapingHtml"
    return re.sub('&(%s);' % '|'.join(name2codepoint),
                  lambda m: unichr(name2codepoint[m.group(1)]), s)
