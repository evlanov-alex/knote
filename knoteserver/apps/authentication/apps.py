from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'knoteserver.apps.authentication'

    def ready(self):
        import knoteserver.apps.authentication.signals
