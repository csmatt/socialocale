from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from models import SubscribeEmail
from django.core.validators import validate_email
import json
class Root(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return TemplateResponse(request, 'main.html')
        else:
            return HttpResponseRedirect('/landing')

class LandingPage(View):
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'landing_page.html')

    def post(self, request, *args, **kwargs):
        response = {'success':True}
        emailAddress = request.POST.get('email')
        try:
            validate_email(emailAddress)
            try:
                SubscribeEmail.objects.create(email=emailAddress)
            except:
                pass # address is already in db
        except Exception, e:
            response = {'error': e.messages[0]}
        return HttpResponse(json.dumps(response), content_type="application/json")
