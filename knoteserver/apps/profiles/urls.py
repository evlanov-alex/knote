from django.urls import path, include
from rest_framework.routers import DefaultRouter

from knoteserver.apps.profiles import views

app_name = 'Profiles'

router = DefaultRouter(trailing_slash=False)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me', views.CurrentUserAPIView.as_view(), name='me'),
]
