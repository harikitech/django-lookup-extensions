from django.db.models.fields.related import ForeignObject
from django.db.models.fields.related_lookups import RelatedLookupMixin

from lookup_extensions.lookups import Complement


class RelatedComplement(RelatedLookupMixin, Complement):
    pass


ForeignObject.register_lookup(RelatedComplement)
