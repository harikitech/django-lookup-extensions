from __future__ import unicode_literals

try:
    from lookup.test_lookups import YearComparisonLookupTests as DjangoYearComparisonLookupTests
except ImportError:
    # Django>=2.0 only
    from django.test import TestCase as DjangoYearComparisonLookupTests


class YearComparisonLookupTests(DjangoYearComparisonLookupTests):
    pass
