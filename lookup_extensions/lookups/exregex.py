from django.db.models.fields import Field
from django.db.models.lookups import Regex


class AbstractExRegexLookup(Regex):
    def process_rhs(self, compiler, connection):
        rhs, params = super(AbstractExRegexLookup, self).process_rhs(compiler, connection)
        if self.rhs_is_direct_value() and params and not self.bilateral_transforms:
            for escape, operator in connection.regex_synonyms.items():
                params[0] = params[0].replace(escape, operator)
        return rhs, params


@Field.register_lookup
class ExRegexLookup(AbstractExRegexLookup):
    lookup_name = 'exregex'


@Field.register_lookup
class ExIRegexLookup(AbstractExRegexLookup):
    lookup_name = 'exiregex'


@Field.register_lookup
class NeExRegexLookup(AbstractExRegexLookup):
    lookup_name = 'neexregex'


@Field.register_lookup
class NeExIRegexLookup(AbstractExRegexLookup):
    lookup_name = 'neexiregex'
