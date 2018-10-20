from django.contrib.auth import get_user_model
from rest_framework import serializers

from knoteserver.apps.profiles.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'name', 'image')
