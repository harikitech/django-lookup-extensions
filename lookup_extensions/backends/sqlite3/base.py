from django.db.backends.sqlite3.base import \
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
            'neiexact': "NOT LIKE %s ESCAPE '\\'",
            'necontains': "NOT LIKE %s ESCAPE '\\'",
            'neicontains': "NOT LIKE %s ESCAPE '\\'",
            'neregex': 'NOT REGEXP %s',
            'neiregex': "NOT REGEXP '(?i)' || %s",
            'nestartswith': "NOT LIKE %s ESCAPE '\\'",
            'neendswith': "NOT LIKE %s ESCAPE '\\'",
            'neistartswith': "NOT LIKE %s ESCAPE '\\'",
            'neiendswith': "NOT LIKE %s ESCAPE '\\'",
            # For exregex
            'exregex': 'REGEXP %s',
            'exiregex': "REGEXP '(?i)' || %s",
            'neexregex': 'NOT REGEXP %s',
            'neexiregex': "NOT REGEXP '(?i)' || %s",
        }
    )
    pattern_ops = merge_dicts(
        DjangoDatabaseWrapper.pattern_ops,
        {
            'necontains': r"NOT LIKE '%%' || {} || '%%' ESCAPE '\'",
            'neicontains': r"NOT LIKE '%%' || UPPER({}) || '%%' ESCAPE '\'",
            'nestartswith': r"NOT LIKE {} || '%%' ESCAPE '\'",
            'neistartswith': r"NOT LIKE UPPER({}) || '%%' ESCAPE '\'",
            'neendswith': r"NOT LIKE '%%' || {} ESCAPE '\'",
            'neiendswith': r"NOT LIKE '%%' || UPPER({}) ESCAPE '\'",
        }
    )
    regex_synonyms = {}


class DatabaseWrapper(ExtendedDatabaseWrapperMixin, DjangoDatabaseWrapper):
    pass
