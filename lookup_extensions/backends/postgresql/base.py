from django.db.backends.postgresql.base import \
    DatabaseWrapper as DjangoDatabaseWrapper

from lookup_extensions.utils import merge_dicts

from .operations import DatabaseOperations


class ExtendedDatabaseWrapperMixin(object):
    ops_class = DatabaseOperations
    operators = merge_dicts(
        DjangoDatabaseWrapper.operators,
        {
            # For negates
            'neexact': '<> %s',
            'neiexact': '<> UPPER(%s)',
            'necontains': 'NOT LIKE %s',
            'neicontains': 'NOT LIKE UPPER(%s)',
            'neregex': '!~ %s',
            'neiregex': '!~* %s',
            'nestartswith': 'NOT LIKE %s',
            'neendswith': 'NOT LIKE %s',
            'neistartswith': 'NOT LIKE UPPER(%s)',
            'neiendswith': 'NOT LIKE UPPER(%s)',
            # For exregex
            'exregex': '~ %s',
            'exiregex': '~* %s',
            'neexregex': '!~ %s',
            'neexiregex': '!~* %s',
        }
    )
    pattern_ops = merge_dicts(
        DjangoDatabaseWrapper.pattern_ops,
        {
           'necontains': r"NOT LIKE '%%' || {} || '%%'",
           'neicontains': r"NOT LIKE '%%' || UPPER({}) || '%%'",
           'nestartswith': r"NOT LIKE {} || '%%'",
           'neistartswith': r"NOT LIKE UPPER({}) || '%%'",
           'neendswith': r"NOT LIKE '%%' || {}",
           'neiendswith': r"NOT LIKE '%%' || UPPER({})",
        }
    )
    regex_synonyms = {
        '\\<': '[[:<:]]',
        '\\>': '[[:>:]]',
    }


class DatabaseWrapper(ExtendedDatabaseWrapperMixin, DjangoDatabaseWrapper):
    pass
