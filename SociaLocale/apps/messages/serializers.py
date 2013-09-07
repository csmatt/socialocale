from rest_framework import serializers
from userena.contrib.umessages.models import Message, MessageContact
from SociaLocale.apps.sl_user.serializers import BasicUserSerializer, BasicUserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('recipients', 'sender_deleted_at')

class MessageContactSerializer(serializers.ModelSerializer):
    latest_message = MessageSerializer()
    from_user = BasicUserSerializer()
    to_user = BasicUserSerializer()
    class Meta:
        model = MessageContact

