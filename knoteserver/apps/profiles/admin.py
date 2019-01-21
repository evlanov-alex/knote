from django.contrib import admin

from knoteserver.apps.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ModelAdmin for editing user profiles."""

    list_display = ('user', 'name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
