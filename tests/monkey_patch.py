from lookup_extensions.manager import Manager

try:
    from lookup.models import (
        Article as LookupArticle,
        Game,
        Player,
        Season,
        Tag,
    )
    from or_lookups.models import (
        Article as OrLookupsArticle,
    )
    from reverse_lookup.models import (
        Choice,
        Poll,
        User,
    )
    from string_lookup.models import (
        Article as StringLookupArticle,
        Bar,
        Base,
        Child,
        Foo,
        Whiz,
    )
except ImportError:
    print("Run tests/bootstrap.py before run tests.")
    raise


def replace_managers():
    for model_cls in [
        Bar,
        Base,
        Child,
        Choice,
        Foo,
        Game,
        LookupArticle,
        OrLookupsArticle,
        Player,
        Poll,
        Season,
        StringLookupArticle,
        Tag,
        User,
        Whiz,
    ]:
        model_cls._meta.local_managers = []
        manager = Manager()
        model_cls.add_to_class('objects', manager)
