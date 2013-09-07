from django.http import HttpResponse
from django.views.generic import View
from userena.contrib.umessages.models import Message, MessageContact
from django.core import serializers
from SociaLocale.apps.sl_user.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.response import Response
from serializers import MessageSerializer, MessageContactSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONPRenderer, JSONRenderer

class Conversation(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        messages = MessageContact.objects.all()
        serializer = MessageContactSerializer(messages, many=True)
        return Response(serializer.data)


class MessageList(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, format='json'):
        messages = MessageContact.objects.get_contacts_for(request.user)#MessageContact.objects.all()
        serializer = MessageContactSerializer(messages, many=True)
        return Response(serializer.data)

class MessageConversationView(APIView):
    renderer_classes = (JSONRenderer, JSONPRenderer)

    def get(self, request, *args, **kwargs):
        messages = Message.objects.get_conversation_between(from_user=request.user.pk, to_user=User.objects.filter(pk=request.GET.get('other_user_id')))
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)