from django.db.models.manager import BaseManager

from .query import QuerySet


class LookupExtensionManager(BaseManager):
    pass


class Manager(LookupExtensionManager.from_queryset(QuerySet)):
    pass
