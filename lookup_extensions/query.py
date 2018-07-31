from django.db.models.query import QuerySet as DjangoQuerySet

from .sql import Query


class QuerySet(DjangoQuerySet):
    def __init__(self, model=None, query=None, **kwargs):
        super(QuerySet, self).__init__(model=model, query=query or Query(model), **kwargs)
