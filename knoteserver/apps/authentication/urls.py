from django.urls import path
from rest_framework.authtoken import views as rest_views

from knoteserver.apps.authentication import views

app_name = 'Authentication'

urlpatterns = [
    path('login', rest_views.obtain_auth_token, name='login'),
    path('register', views.RegistrationAPIView.as_view(), name='register'),
]
