from django.db.backends.postgresql.operations import \
    DatabaseOperations as DjangoDatabaseOperations

from lookup_extensions.backends.base.operations import (
    ExtendedDatabaseOperationsMixin,
)


class DatabaseOperations(ExtendedDatabaseOperationsMixin, DjangoDatabaseOperations):
    pass
