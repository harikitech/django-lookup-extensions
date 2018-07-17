try:
    from lookup.test_decimalfield import DecimalFieldLookupTests as DjangoDecimalFieldLookupTests
except ImportError:
    import sys
    sys.exit("Run tests/bootstrap.py before run tests.")


class DecimalFieldLookupTests(DjangoDecimalFieldLookupTests):
    pass
