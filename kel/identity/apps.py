from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "kel.identity"
    label = "kel_identity"

    def ready(self):
        import_module("kel.identity.receivers")
