from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'knoteserver.apps.authentication'

    def ready(self):
        from knoteserver.apps.authentication import signals  # noqa: F401
