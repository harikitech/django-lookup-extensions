from django.db.models.manager import BaseManager

from .query import QuerySet


class Manager(BaseManager.from_queryset(QuerySet)):
    def __init__(self):
        super(Manager, self).__init__()
