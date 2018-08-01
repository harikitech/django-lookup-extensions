from django.db.models.expressions import Exists
from django.db.models.fields.related import ForeignObject
from django.db.models.fields.related_lookups import RelatedLookupMixin
from django.db.models.lookups import Lookup


@ForeignObject.register_lookup
class RelatedExists(RelatedLookupMixin, Lookup):
    lookup_name = 'exists'

    def __init__(self, lhs, rhs):
        return super(RelatedExists, self).__init__(lhs, rhs)

    def get_prep_lookup(self):
        return self.rhs

    def process_lhs(self, compiler, connection, lhs=None):
        return '', []

    def get_rhs_op(self, connection, rhs):
        return Exists.template % {'subquery': rhs}

    def as_sql(self, compiler, connection):
        return '', []
