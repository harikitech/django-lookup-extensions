from django.apps import AppConfig


class LookupExtensionsConfig(AppConfig):
    name = 'lookup_extensions'

    def ready(self):
        from . import lookups  # noqa F401
