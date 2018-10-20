from django.contrib import admin

from knoteserver.apps.profiles.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
