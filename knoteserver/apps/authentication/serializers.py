from django.contrib.auth import get_user_model
from rest_framework import serializers

from knoteserver.apps.profiles.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Profile.objects.create(user=user, name=user.username)
        return user
