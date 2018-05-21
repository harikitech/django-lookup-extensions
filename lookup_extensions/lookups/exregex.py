# -*- coding: utf-8 -*-

from django.db.models.fields import Field
from django.db.models.lookups import (
    FieldGetDbPrepValueMixin,
    Lookup,
)

VENDOR_DIALECT = {
    'mysql': {
        'operators': {
            'exregex': 'REGEXP BINARY %s',
            'exiregex': 'REGEXP %s',
            'neexregex': 'NOT REGEXP BINARY %s',
            'neexiregex': 'NOT REGEXP %s',
        },
    },
    'postgresql': {
        'operators': {
            'exregex': '~ %s',
            'exiregex': '~* %s',
            'neexregex': '!~ %s',
            'neexiregex': '!~* %s',
        },
    },
    'sqlite': {
        'operators': {
            'exregex': 'REGEXP %s',
            'exiregex': "REGEXP '(?i)' || %s",
            'neexregex': 'NOT REGEXP %s',
            'neexiregex': "NOT REGEXP '(?i)' || %s",
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
    'sqlite': {
            # '\\<': '\\b',  # \\< means `start of word`, \\b means word boundary
            # '\\>': '\\b',  # \\> means `end of word`, \\b means word boundary
    },
}
for vendor in VENDOR_SYNONYMS.keys():
    expressions = []
    for expression in VENDOR_SYNONYMS[vendor]:
        expressions.append(expression)
    VENDOR_SYNONYMS[vendor]['expressions'] = expressions

VENDOR_SYNONYMS['redshift'] = VENDOR_SYNONYMS['postgresql']


class AbstractExRegexLookup(FieldGetDbPrepValueMixin, Lookup):
    def lookup_operator(self):
        raise NotImplementedError()

    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super(AbstractExRegexLookup, self).process_lhs(
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
        rhs, params = super(AbstractExRegexLookup, self).process_rhs(qn, connection)
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
class ExRegexLookup(AbstractExRegexLookup):
    lookup_name = 'exregex'


@Field.register_lookup
class ExIRegexLookup(AbstractExRegexLookup):
    lookup_name = 'exiregex'


@Field.register_lookup
class NeExRegexLookup(AbstractExRegexLookup):
    lookup_name = 'neexregex'


@Field.register_lookup
class NeExIRegexLookup(AbstractExRegexLookup):
    lookup_name = 'neexiregex'
