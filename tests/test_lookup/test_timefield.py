try:
    from lookup.test_timefield import TimeFieldLookupTests as DjangoTimeFieldLookupTests
except ImportError:
    import sys
    sys.exit("Run tests/bootstrap.py before run tests.")


class TimeFieldLookupTests(DjangoTimeFieldLookupTests):
    pass
