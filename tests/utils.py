from django.db import connection
from django.test.testcases import _deferredSkip


def skipIfDBVendor(*vendors):
    return _deferredSkip(
        lambda: any(connection.vendor == vendor for vendor in vendors),
        "Database has vendor(s) %s" % ", ".join(vendors)
    )
