from rest_framework import response, permissions, views, status
from rest_framework.authtoken.models import Token

from knoteserver.apps.authentication.serializers import RegistrationSerializer


class RegistrationAPIView(views.APIView):
    """API view for registration."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):  # noqa: D102
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        serialized_data = serializer.data
        serialized_data['token'] = token.key
        return response.Response(serialized_data, status=status.HTTP_201_CREATED)
