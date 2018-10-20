from django.contrib import admin

# Register your models here.
from django.contrib import admin

from knoteserver.apps.notes.models import *


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'tag_list', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
