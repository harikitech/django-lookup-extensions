# -*- coding: utf-8 -*-

from django.db.models.fields import Field
from django.db.models.lookups import (
    FieldGetDbPrepValueMixin,
    Lookup,
)

VENDOR_DIALECT = {
    'mysql': {
        'operators': {
            'neexact': '<> %s',
            'neiexact': 'NOT LIKE %s',
            'necontains': 'NOT LIKE BINARY %s',
            'neicontains': 'NOT LIKE %s',
            'nestartswith': 'NOT LIKE BINARY %s',
            'neendswith': 'NOT LIKE BINARY %s',
            'neistartswith': 'NOT LIKE %s',
            'neiendswith': 'NOT LIKE %s',
            'neregex': 'NOT REGEXP BINARY %s',
            'neiregex': 'NOT REGEXP %s',
        },
        'pattern_ops': {
            'necontains': "NOT LIKE BINARY CONCAT('%%', {}, '%%')",  # noqa P103
            'neicontains': "NOT LIKE CONCAT('%%', {}, '%%')",  # noqa P103
            'nestartswith': "NOT LIKE BINARY CONCAT({}, '%%')",  # noqa P103
            'neistartswith': "NOT LIKE CONCAT({}, '%%')",  # noqa P103
            'neendswith': "NOT LIKE BINARY CONCAT('%%', {})",  # noqa P103
            'neiendswith': "NOT LIKE CONCAT('%%', {})",  # noqa P103
        },
    },
    'postgresql': {
        'operators': {
            'neexact': '<> %s',
            'neiexact': '<> UPPER(%s)',
            'necontains': 'NOT LIKE %s',
            'neicontains': 'NOT LIKE UPPER(%s)',
            'nestartswith': 'NOT LIKE %s',
            'neendswith': 'NOT LIKE %s',
            'neistartswith': 'NOT LIKE UPPER(%s)',
            'neiendswith': 'NOT LIKE UPPER(%s)',
            'neregex': '!~ %s',
            'neiregex': '!~* %s',
        },
        'pattern_ops': {
            'necontains': "NOT LIKE '%%' || {} || '%%'",  # noqa P103
            'neicontains': "NOT LIKE '%%' || UPPER({}) || '%%'",  # noqa P103
            'nestartswith': "NOT LIKE {} || '%%'",  # noqa P103
            'neistartswith': "NOT LIKE UPPER({}) || '%%'",  # noqa P103
            'neendswith': "NOT LIKE '%%' || {}",  # noqa P103
            'neiendswith': "NOT LIKE '%%' || UPPER({})",  # noqa P103
        },
    },
    'sqlite': {
        'operators': {
            'neexact': '<> %s',
            'neiexact': "NOT LIKE %s ESCAPE '\\'",
            'necontains': "NOT LIKE %s ESCAPE '\\'",
            'neicontains': "NOT LIKE %s ESCAPE '\\'",
            'nestartswith': "NOT LIKE %s ESCAPE '\\'",
            'neendswith': "NOT LIKE %s ESCAPE '\\'",
            'neistartswith': "NOT LIKE %s ESCAPE '\\'",
            'neiendswith': "NOT LIKE %s ESCAPE '\\'",
            'neregex': 'NOT REGEXP %s',
            'neiregex': "NOT REGEXP '(?i)' || %s",
        },
        'pattern_ops': {
            'necontains': r"NOT LIKE '%%' || {} || '%%' ESCAPE '\'",  # noqa P103
            'neicontains': r"NOT LIKE '%%' || UPPER({}) || '%%' ESCAPE '\'",  # noqa P103
            'nestartswith': r"NOT LIKE {} || '%%' ESCAPE '\'",  # noqa P103
            'neistartswith': r"NOT LIKE UPPER({}) || '%%' ESCAPE '\'",  # noqa P103
            'neendswith': r"NOT LIKE '%%' || {} ESCAPE '\'",  # noqa P103
            'neiendswith': r"NOT LIKE '%%' || UPPER({}) ESCAPE '\'",  # noqa P103
        },
    },
}
VENDOR_DIALECT['redshift'] = VENDOR_DIALECT['postgresql']


class NeLookup(Lookup):
    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super(NeLookup, self).process_lhs(
            compiler,
            connection,
            lhs,
        )
        field_internal_type = self.lhs.output_field.get_internal_type()
        # NeLookup's lookup_name looks like neexact and it starts with `ne`.
        # Strip `ne` from neiexact, it is iexact and lookup_cast returns `UPPER(%s) except mysql.`.
        lhs_sql = connection.ops.lookup_cast(self.lookup_name[2:], field_internal_type) % lhs_sql
        return lhs_sql, list(params)

    def as_sql(self, compiler, connection):
        lhs_sql, params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        params.extend(rhs_params)
        rhs_sql = self.get_rhs_op(connection, rhs_sql)
        return '%s %s' % (lhs_sql, rhs_sql), params

    def get_rhs_op(self, connection, rhs):
        return VENDOR_DIALECT[connection.vendor]['operators'][self.lookup_name] % rhs


@Field.register_lookup
class NeExact(FieldGetDbPrepValueMixin, NeLookup):
    lookup_name = 'neexact'


@Field.register_lookup
class NeIExact(NeLookup):
    lookup_name = 'neiexact'
    prepare_rhs = False

    def process_rhs(self, qn, connection):
        rhs, params = super(NeIExact, self).process_rhs(qn, connection)
        if params:
            params[0] = connection.ops.prep_for_iexact_query(params[0])
        return rhs, params


class NePatternLookup(NeLookup):

    def get_rhs_op(self, connection, rhs):
        if hasattr(self.rhs, 'get_compiler') or hasattr(self.rhs, 'as_sql') or self.bilateral_transforms:
            pattern = VENDOR_DIALECT[connection.vendor]['pattern_ops'][self.lookup_name].format(connection.pattern_esc)
            return pattern.format(rhs)
        else:
            return super(NePatternLookup, self).get_rhs_op(connection, rhs)


@Field.register_lookup
class NeContains(NePatternLookup):
    lookup_name = 'necontains'
    prepare_rhs = False

    def process_rhs(self, qn, connection):
        rhs, params = super(NeContains, self).process_rhs(qn, connection)
        if params and not self.bilateral_transforms:
            params[0] = "%%%s%%" % connection.ops.prep_for_like_query(params[0])
        return rhs, params


@Field.register_lookup
class NeIContains(NeContains):
    lookup_name = 'neicontains'
    prepare_rhs = False


@Field.register_lookup
class NeStartsWith(NePatternLookup):
    lookup_name = 'nestartswith'
    prepare_rhs = False

    def process_rhs(self, qn, connection):
        rhs, params = super(NeStartsWith, self).process_rhs(qn, connection)
        if params and not self.bilateral_transforms:
            params[0] = "%s%%" % connection.ops.prep_for_like_query(params[0])
        return rhs, params


@Field.register_lookup
class NeIStartsWith(NePatternLookup):
    lookup_name = 'neistartswith'
    prepare_rhs = False

    def process_rhs(self, qn, connection):
        rhs, params = super(NeIStartsWith, self).process_rhs(qn, connection)
        if params and not self.bilateral_transforms:
            params[0] = "%s%%" % connection.ops.prep_for_like_query(params[0])
        return rhs, params


@Field.register_lookup
class NeEndsWith(NePatternLookup):
    lookup_name = 'neendswith'
    prepare_rhs = False

    def process_rhs(self, qn, connection):
        rhs, params = super(NeEndsWith, self).process_rhs(qn, connection)
        if params and not self.bilateral_transforms:
            params[0] = "%%%s" % connection.ops.prep_for_like_query(params[0])
        return rhs, params


@Field.register_lookup
class NeIEndsWith(NePatternLookup):
    lookup_name = 'neiendswith'
    prepare_rhs = False

    def process_rhs(self, qn, connection):
        rhs, params = super(NeIEndsWith, self).process_rhs(qn, connection)
        if params and not self.bilateral_transforms:
            params[0] = "%%%s" % connection.ops.prep_for_like_query(params[0])
        return rhs, params


@Field.register_lookup
class NeRegex(NeLookup):
    lookup_name = 'neregex'
    prepare_rhs = False


@Field.register_lookup
class NeIRegex(NeRegex):
    lookup_name = 'neiregex'
