from django.db import models
from taggit.managers import TaggableManager

from knoteserver.apps.core.models import TimestampedModel


class Note(TimestampedModel):
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=512, blank=True)
    text = models.TextField()
    tags = TaggableManager(related_name='notes', blank=True)
    allowed_profiles = models.ManyToManyField(
        'profiles.Profile',
        through='NoteAccess',
        related_name='available_notes',
        blank=True
    )

    def __str__(self):
        return 'Note: %s - %s' % (self.author.user.username, self.text[:20])


class NoteAccess(TimestampedModel):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    can_write = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at', '-updated_at')
        unique_together = ('note', 'profile')
