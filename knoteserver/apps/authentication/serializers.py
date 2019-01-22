from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):  # noqa: D102
        user = get_user_model().objects.create_user(**validated_data)
        return user
