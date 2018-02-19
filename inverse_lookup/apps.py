from django.apps import AppConfig


class InverseLookupConfig(AppConfig):
    name = 'inverse_lookup'

    def ready(self):
        from . import lookups  # noqa F401
