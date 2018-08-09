from django.db.models import Exists
from django.db.models.fields import Field
from django.db.models.lookups import (
    BuiltinLookup,
    FieldGetDbPrepValueMixin,
)


@Field.register_lookup
class Complement(FieldGetDbPrepValueMixin, BuiltinLookup):
    lookup_name = 'complement'

    def process_rhs(self, compiler, connection):
        if self.rhs_is_direct_value() or not isinstance(self.rhs, Exists):
            raise ValueError("Exists subqueries are required")

        db_rhs = getattr(self.rhs, '_db', None)
        if db_rhs is not None and db_rhs != connection.alias:
            raise ValueError("Subqueries aren't allowed across different databases")

        return super(Complement, self).process_rhs(compiler, connection)

    def as_sql(self, compiler, connection):
        return self.process_rhs(compiler, connection)
