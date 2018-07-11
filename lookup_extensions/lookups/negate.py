from django.db.models.fields import Field
from django.db.models.lookups import (
    Contains,
    EndsWith,
    Exact,
    IEndsWith,
    IExact,
    IRegex,
    IStartsWith,
    Regex,
    StartsWith,
)


@Field.register_lookup
class NeExact(Exact):
    lookup_name = 'neexact'


@Field.register_lookup
class NeIExact(IExact):
    lookup_name = 'neiexact'


@Field.register_lookup
class NeContains(Contains):
    lookup_name = 'necontains'


@Field.register_lookup
class NeIContains(NeContains):
    lookup_name = 'neicontains'


@Field.register_lookup
class NeStartsWith(StartsWith):
    lookup_name = 'nestartswith'


@Field.register_lookup
class NeIStartsWith(IStartsWith):
    lookup_name = 'neistartswith'


@Field.register_lookup
class NeEndsWith(EndsWith):
    lookup_name = 'neendswith'


@Field.register_lookup
class NeIEndsWith(IEndsWith):
    lookup_name = 'neiendswith'


@Field.register_lookup
class NeRegex(Regex):
    lookup_name = 'neregex'


@Field.register_lookup
class NeIRegex(IRegex):
    lookup_name = 'neiregex'
