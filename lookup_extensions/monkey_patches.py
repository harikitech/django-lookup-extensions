from django.db import utils

from .backends.mixins import ExtendedDatabaseOperationsMixin
from .backends.mysql import ExtendedDatabaseWrapper as MySQLExtendedDatabaseWrapper
from .backends.postgresql import ExtendedDatabaseWrapper as PostgreSQLExtendedDatabaseWrapper
from .backends.sqlite3 import ExtendedDatabaseWrapper as SQLite3ExtendedDatabaseWrapper


def patche_ops_class(original_ops_class):
    if issubclass(original_ops_class, ExtendedDatabaseOperationsMixin):
        return original_ops_class

    class DatabaseOperations(ExtendedDatabaseOperationsMixin, original_ops_class):
        pass
    return DatabaseOperations


def patch_operators(original_database_wrapper_class):
    def _extend_wrapper(extended_wrapper_class):
        original_database_wrapper_class.operators.update(extended_wrapper_class.operators)
        original_database_wrapper_class.pattern_ops.update(extended_wrapper_class.pattern_ops)
        original_database_wrapper_class.regex_synonyms = extended_wrapper_class.regex_synonyms

    if original_database_wrapper_class.vendor == 'mysql':
        _extend_wrapper(MySQLExtendedDatabaseWrapper)
    elif original_database_wrapper_class.vendor in ['postgres', 'redshift']:
        _extend_wrapper(PostgreSQLExtendedDatabaseWrapper)
    elif original_database_wrapper_class.vendor == 'sqlite':
        _extend_wrapper(SQLite3ExtendedDatabaseWrapper)
    return original_database_wrapper_class


def patch_load_backend():
    def load_backend(backend_name):
        backend = original_load_backend(backend_name)
        backend.DatabaseWrapper.ops_class = patche_ops_class(backend.DatabaseWrapper.ops_class)
        backend.DatabaseWrapper = patch_operators(backend.DatabaseWrapper)
        return backend

    original_load_backend = utils.load_backend
    utils.load_backend = load_backend
