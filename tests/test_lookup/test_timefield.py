from __future__ import unicode_literals

try:
    from lookup.test_timefield import TimeFieldLookupTests as DjangoTimeFieldLookupTests
except ImportError:
    print("Run tests/bootstrap.py before run tests.")


class TimeFieldLookupTests(DjangoTimeFieldLookupTests):
    pass
