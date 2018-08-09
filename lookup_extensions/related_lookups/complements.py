from django.db.models.fields.related_lookups import (
    get_normalized_value,
    MultiColSource,
    RelatedLookupMixin,
)
from django.db.models.fields.related import ForeignObject

from lookup_extensions.lookups import Complement


class RelatedComplement(RelatedLookupMixin, Complement):
    pass


ForeignObject.register_lookup(RelatedComplement)
