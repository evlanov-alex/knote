from django.urls import path, include
from rest_framework.routers import DefaultRouter

from knoteserver.apps.profiles.views import ProfileViewSet

app_name = 'Profiles'

router = DefaultRouter(trailing_slash=False)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
