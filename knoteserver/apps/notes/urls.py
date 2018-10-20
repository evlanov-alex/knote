from django.urls import path, include
from rest_framework.routers import DefaultRouter

from knoteserver.apps.notes.views import NoteViewSet

app_name = 'Notes'

router = DefaultRouter(trailing_slash=False)
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
