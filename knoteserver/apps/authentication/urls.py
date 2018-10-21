from django.urls import path
from rest_framework.authtoken import views

from knoteserver.apps.authentication.views import RegistrationAPIView

app_name = 'Authentication'

urlpatterns = [
    path('login', views.obtain_auth_token, name='login'),
    path('register', RegistrationAPIView.as_view(), name='register'),
]
