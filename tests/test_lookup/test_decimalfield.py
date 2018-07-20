from __future__ import unicode_literals

try:
    from lookup.test_decimalfield import DecimalFieldLookupTests as DjangoDecimalFieldLookupTests
except ImportError:
    print("Run tests/bootstrap.py before run tests.")
    raise


class DecimalFieldLookupTests(DjangoDecimalFieldLookupTests):
    pass
