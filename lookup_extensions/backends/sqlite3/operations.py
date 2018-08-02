from django.db.backends.sqlite3.operations import \
    DatabaseOperations as DjangoDatabaseOperations

from lookup_extensions.backends.base.operations import (
    ExtendedDatabaseOperationsMixin,
)


class DatabaseOperations(ExtendedDatabaseOperationsMixin, DjangoDatabaseOperations):
    pass
