from rest_framework import serializers
from models import UserProfile, UserSettings
from django.contrib.auth.models import User
from SociaLocale.apps.interests.serializers import InterestSerializer
from SociaLocale.apps.interests.models import Interest

class LocationField(serializers.RelatedField):
    def to_native(self, point_field):
        """
        Return {lat: latitude, lon: longitude}
        """
        return {'lat': point_field.coords[0], 'lon': point_field.coords[1]}

class SelectedInterestField(serializers.RelatedField):
    def field_to_native(self, obj, field_name):
        pass

class BasicUserProfileSerializer(serializers.ModelSerializer):
    location = LocationField()
    class Meta:
        model = UserProfile
        fields = ('mugshot', 'location',)

class BasicUserSerializer(serializers.ModelSerializer):
    profile = BasicUserProfileSerializer()
    class Meta:
        model = User
        fields = ('profile', 'username', 'first_name', 'last_name', 'id')


class FullUserProfileSerializer(serializers.ModelSerializer):
    #location = LocationField()
    class Meta:
        model = UserProfile
        fields = ('mugshot', 'location', 'interests')

class FullUserSerializer(serializers.ModelSerializer):
    profile = FullUserProfileSerializer()

    class Meta:
        model = User
        fields = ('profile', 'username', 'first_name', 'last_name', 'id')


class MeUserSettingsSerializer(serializers.ModelSerializer):
    #location = LocationField()
    class Meta:
        model = UserSettings

class MeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'is_superuser', 'user_permissions', 'groups', 'date_joined', 'last_login')

class MeProfileSerializer(serializers.ModelSerializer):
    user = MeUserSerializer()
    settings = MeUserSettingsSerializer()
    interests = InterestSerializer(many=True)
    location = LocationField()
    selectedInterest = InterestSerializer()

    class Meta:
        model = UserProfile
        exclude = ('privacy',)

