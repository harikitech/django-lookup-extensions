# -*- coding: utf-8 -*-

from django.db.models.fields import Field
from django.db.models.lookups import (
    FieldGetDbPrepValueMixin,
    Lookup,
)

VENDOR_DIALECT = {
    'mysql': {
        'operators': {
            'regex': 'REGEXP BINARY %s',
            'iregex': 'REGEXP %s',
            'neregex': 'NOT REGEXP BINARY %s',
            'neiregex': 'NOT REGEXP %s',
        },
    },
    'postgresql': {
        'operators': {
            'regex': '~ %s',
            'iregex': '~* %s',
            'neregex': '!~ %s',
            'neiregex': '!~* %s',
        },
    },
}
VENDOR_DIALECT['redshift'] = VENDOR_DIALECT['postgresql']


VENDOR_SYNONYMS = {
    'postgresql': {
            '\\<': '[[:<:]]',
            '\\>': '[[:>:]]',
    },
    'mysql': {
            '\\<': '[[:<:]]',
            '\\>': '[[:>:]]',
            '\\d': '[[:digit:]]',
            '\\D': '[^[:digit:]]',
            '\\w': '[[:alnum:]_]',
            '\\W': '[^[:alnum:]_]',
            '\\s': '[[:space:]]',
            '\\S': '[^[:space:]]',
    },
}
for vendor in VENDOR_SYNONYMS.keys():
    expressions = []
    for expression in VENDOR_SYNONYMS[vendor]:
        expressions.append(expression)
    VENDOR_SYNONYMS[vendor]['expressions'] = expressions

VENDOR_SYNONYMS['redshift'] = VENDOR_SYNONYMS['postgresql']


class AbstractRegexLookup(FieldGetDbPrepValueMixin, Lookup):
    def lookup_operator(self):
        raise NotImplementedError()

    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super(AbstractRegexLookup, self).process_lhs(
            compiler,
            connection,
            lhs,
        )
        lhs_sql = '%s' % lhs_sql
        return lhs_sql, list(params)

    def as_sql(self, compiler, connection):
        lhs_sql, params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        params.extend(rhs_params)
        rhs_sql = self.get_rhs_op(connection, rhs_sql)
        return '%s %s' % (lhs_sql, rhs_sql), params

    def process_rhs(self, qn, connection):
        rhs, params = super(AbstractRegexLookup, self).process_rhs(qn, connection)
        param = params[0]
        if params and not self.bilateral_transforms:
            for expression in VENDOR_SYNONYMS[connection.vendor]['expressions']:
                param = param.replace(
                    expression,
                    VENDOR_SYNONYMS[connection.vendor][expression],
                )
            params[0] = param
        return rhs, params

    def get_rhs_op(self, connection, rhs):
        return VENDOR_DIALECT[connection.vendor]['operators'][self.__class__.lookup_name] % rhs


@Field.register_lookup
class RegexLookup(AbstractRegexLookup):
    lookup_name = 'regex'


@Field.register_lookup
class IRegexLookup(AbstractRegexLookup):
    lookup_name = 'iregex'


@Field.register_lookup
class NeRegexLookup(AbstractRegexLookup):
    lookup_name = 'neregex'


@Field.register_lookup
class NeIRegexLookup(AbstractRegexLookup):
    lookup_name = 'neiregex'
