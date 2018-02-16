from django.apps import AppConfig
from . import lookups

class InverseLookupConfig(AppConfig):
    name = 'inverse_lookup'

    def ready(self):
        from . import lookups
