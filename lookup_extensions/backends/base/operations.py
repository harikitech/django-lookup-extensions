# Load lookup types
from lookup_extensions import lookups  # noqa F401


class ExtendedDatabaseOperationsMixin(object):
    NEGATE_REGULAR_LOOKUP_TYPES = {
        'neexact': 'exact',
        'neiexact': 'iexact',
        'necontains': 'contains',
        'neicontains': 'icontains',
        'neregex': 'regex',
        'neiregex': 'iregex',
        'exregex': 'regex',
        'exiregex': 'iregex',
        'neexregex': 'regex',
        'neexiregex': 'iregex',
        'nestartswith': 'startswith',
        'neistartswith': 'istartswith',
        'neendswith': 'endswith',
        'neiendswith': 'iendswith',
    }

    def convert_to_regular_lookup_type(self, lookup_type):
        return self.NEGATE_REGULAR_LOOKUP_TYPES.get(lookup_type, None)

    def lookup_cast(self, lookup_type, internal_type=None):
        regular_lookup_type = self.convert_to_regular_lookup_type(lookup_type)
        if regular_lookup_type:
            return super(ExtendedDatabaseOperationsMixin, self).lookup_cast(
                regular_lookup_type, internal_type=internal_type)
        return super(ExtendedDatabaseOperationsMixin, self).lookup_cast(
            lookup_type, internal_type=internal_type)
