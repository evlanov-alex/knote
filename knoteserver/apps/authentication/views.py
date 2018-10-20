from rest_framework import response, permissions, views, status
from rest_framework.authtoken.models import Token

from knoteserver.apps.authentication.serializers import RegistrationSerializer


class RegistrationAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data['token'] = token.key

        return response.Response(data, status=status.HTTP_201_CREATED)
