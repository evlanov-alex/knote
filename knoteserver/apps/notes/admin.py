from django.contrib import admin

from knoteserver.apps.notes.models import Note, NoteAccess


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """ModelAdmin for managing notes."""

    list_display = ('author', 'title', 'tag_list', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        """Return Notes QuerySet with prefetched tags."""
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, note: Note):
        """Return list of tags for current Note. Required for list_display."""
        return ', '.join(note.name for note in note.tags.all())


@admin.register(NoteAccess)
class NoteAccessAdmin(admin.ModelAdmin):
    """ModelAdmin for controlling acces to Notes."""

    list_display = ('note', 'profile', 'can_write', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
