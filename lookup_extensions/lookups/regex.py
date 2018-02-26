# -*- coding: utf-8 -*-

from django.db.models.fields import Field
from django.db.models.lookups import (
    FieldGetDbPrepValueMixin,
    Lookup,
)

VENDOR_SYNONYMS = {
    'postgresql': {
            '\\<': '[[:<:]]',
            '\\>': '[[:>:]]',
    },
    'redshift': {
            '\\<': '[[:<:]]',
            '\\>': '[[:>:]]',
            # '\\d': '[[:digit:]]',
            # '\\D': '[^[:digit:]]',
            # '\\w': '[[:word:]]',
            # '\\W': '[^[:word:]]',
            # '\\s': '[[:space:]]',
            # '\\S': '[^[:space:]]',
    }
}
for vendor in VENDOR_SYNONYMS.keys():
    expressions = []
    for expression in VENDOR_SYNONYMS[vendor]:
        expressions.append(expression)
    VENDOR_SYNONYMS[vendor]['expressions'] = expressions

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

    def process_rhs(self, qn, connection):
        rhs, params = super().process_rhs(qn, connection)
        param = params[0]
        if params and not self.bilateral_transforms:
            for expression in VENDOR_SYNONYMS[connection.vendor]['expressions']:
                param = param.replace(
                    expression,
                    VENDOR_SYNONYMS[connection.vendor][expression],
                )
            params[0] = param
        return rhs, params


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
