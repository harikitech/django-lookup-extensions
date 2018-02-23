# -*- coding: utf-8 -*-

from django.db.models.fields import Field
from django.db.models.lookups import (
    FieldGetDbPrepValueMixin,
    Lookup,
)

class AbstractRegexLookup(Lookup):
    def lookup_operator(self):
        raise NotImplementedError()

    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super(AbstractRegexLookup, self).process_lhs(
            compiler,
            connection,
            lhs,
        )
        field_internal_type = self.lhs.output_field.get_internal_type()
        lhs_sql = '%s' % lhs_sql
        return lhs_sql, list(params)

    def as_sql(self, compiler, connection):
        lhs_sql, params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        params.extend(rhs_params)
        rhs_sql = self.get_rhs_op(connection, rhs_sql)
        return '%s %s' % (lhs_sql, rhs_sql), params

    def get_rhs_op(self, connection, rhs):
        return self.lookup_operator() % rhs

@Field.register_lookup
class RegexLookup(AbstractRegexLookup):
    lookup_name = 'regex'

    def lookup_operator(self):
        return '~ %s'

@Field.register_lookup
class NeRegexLookup(AbstractRegexLookup):
    lookup_name = 'neregex'

    def lookup_operator(self):
        return '!~ %s'
