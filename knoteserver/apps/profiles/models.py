from django.contrib.auth import get_user_model
from django.db import models

from knoteserver.apps.core.models import TimestampedModel


class Profile(TimestampedModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return 'Profile: {username}'.format(username=self.user.username)
