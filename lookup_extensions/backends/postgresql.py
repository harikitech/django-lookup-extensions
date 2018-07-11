class ExtendedDatabaseWrapper(object):
    operators = {
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
    }

    pattern_ops = {
       'necontains': r"NOT LIKE '%%' || {} || '%%'",
       'neicontains': r"NOT LIKE '%%' || UPPER({}) || '%%'",
       'nestartswith': r"NOT LIKE {} || '%%'",
       'neistartswith': r"NOT LIKE UPPER({}) || '%%'",
       'neendswith': r"NOT LIKE '%%' || {}",
       'neiendswith': r"NOT LIKE '%%' || UPPER({})",
    }
