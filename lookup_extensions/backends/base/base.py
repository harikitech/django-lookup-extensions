from django.utils.six import add_metaclass


class ExtendedDatabaseWrapperMeta(object):
    def __new__(cls, *args, **kwargs):
        database_wrapper = super(ExtendedDatabaseWrapperMeta, cls).__new__(cls, *args, **kwargs)
        database_wrapper.operations.update(database_wrapper.extended_operations)
        database_wrapper.pattern_ops.update(database_wrapper.pattern_ops)
        return database_wrapper


@add_metaclass(ExtendedDatabaseWrapperMeta)
class BaseExtendedDatabaseWrapper(object):
    extended_operations = set()
    extended_pattern_ops = set()
    regex_synonyms = {}
