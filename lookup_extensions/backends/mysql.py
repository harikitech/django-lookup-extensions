class ExtendedDatabaseWrapper(object):
    operators = {
        # For negates
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
        # For exregex
        'exregex': 'REGEXP BINARY %s',
        'exiregex': 'REGEXP %s',
        'neexregex': 'NOT REGEXP BINARY %s',
        'neexiregex': 'NOT REGEXP %s',
    }

    pattern_ops = {
        'necontains': "NOT LIKE BINARY CONCAT('%%', {}, '%%')",
        'neicontains': "NOT LIKE CONCAT('%%', {}, '%%')",
        'nestartswith': "NOT LIKE BINARY CONCAT({}, '%%')",
        'neistartswith': "NOT LIKE CONCAT({}, '%%')",
        'neendswith': "NOT LIKE BINARY CONCAT('%%', {})",
        'neiendswith': "NOT LIKE CONCAT('%%', {})",
    }

    regex_synonyms = {
        '\\<': '[[:<:]]',
        '\\>': '[[:>:]]',
        '\\d': '[[:digit:]]',
        '\\D': '[^[:digit:]]',
        '\\w': '[[:alnum:]_]',
        '\\W': '[^[:alnum:]_]',
        '\\s': '[[:space:]]',
        '\\S': '[^[:space:]]',
    }
