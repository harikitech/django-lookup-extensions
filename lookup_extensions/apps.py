from django.apps import AppConfig

from .monkey_patches import patch_load_backend

patch_load_backend()


class LookupExtensionsConfig(AppConfig):
    name = 'lookup_extensions'

    def ready(self):
        from . import lookups  # noqa F401
