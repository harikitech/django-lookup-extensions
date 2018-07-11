class ExtendedDatabaseWrapper(object):
    operators = {
        'neexact': '<> %s',
        'neiexact': 'NOT LIKE %s',
        'necontains': 'NOT LIKE BINARY %s',
        'neicontains': 'NOT LIKE %s',
        'neregex': 'NOT REGEXP BINARY %s',
        'neiregex': 'NOT REGEXP %s',
        'nestartswith': 'NOT LIKE BINARY %s',
        'neendswith': 'NOT LIKE BINARY %s',
        'neistartswith': 'NOT LIKE %s',
        'neiendswith': 'NOT LIKE %s',
    }

    pattern_ops = {
        'necontains': "NOT LIKE BINARY CONCAT('%%', {}, '%%')",
        'neicontains': "NOT LIKE CONCAT('%%', {}, '%%')",
        'nestartswith': "NOT LIKE BINARY CONCAT({}, '%%')",
        'neistartswith': "NOT LIKE CONCAT({}, '%%')",
        'neendswith': "NOT LIKE BINARY CONCAT('%%', {})",
        'neiendswith': "NOT LIKE CONCAT('%%', {})",
    }
