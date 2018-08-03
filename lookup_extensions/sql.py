from django.core.exceptions import FieldError
from django.db.models import Exists
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql import Query as DjangoQuery


class ExtendedQueryMixin(object):
    SUBQUERY_LOOKUPS = (
        'exists',
        'neexists',
    )

    def build_lookup(self, lookups, lhs, rhs):
        if lookups and lookups[-1] in self.SUBQUERY_LOOKUPS:
            if not isinstance(rhs, Exists):
                raise FieldError("Value is not Subquery instance.")
            return super(ExtendedQueryMixin, self).build_lookup(['exact'], rhs, not lookups[-1].startswith('ne'))
        return super(ExtendedQueryMixin, self).build_lookup(lookups, lhs, rhs)

    def prepare_lookup_value(self, value, lookups, can_reuse, allow_joins=True):
        if lookups and lookups[-1] in self.SUBQUERY_LOOKUPS:
            value = value.resolve_expression(self, allow_joins=True, reuse=None, summarize=False)
            return value, lookups, []
        return super(ExtendedQueryMixin, self).prepare_lookup_value(
            value, lookups, can_reuse, allow_joins=allow_joins)

    def solve_lookup_type(self, lookup):
        lookup_splitted = lookup.split(LOOKUP_SEP)
        if lookup_splitted and lookup_splitted[-1] in self.SUBQUERY_LOOKUPS:
            return lookup_splitted, (), True  # No JOIN
        return super(ExtendedQueryMixin, self).solve_lookup_type(lookup)


class Query(ExtendedQueryMixin, DjangoQuery):
    pass
