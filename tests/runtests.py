#!/usr/bin/env python

import os
import sys

import django

from .bootstrap import DJANGO_TEST_APP_PATH

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'test_settings')
sys.path.append(os.path.abspath(DJANGO_TEST_APP_PATH))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def runtests():
    from django.conf import settings
    from django.test.utils import get_runner

    django.setup()

    from .monkey_patch import replace_managers

    replace_managers()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=2,
        interactive=False,
        keepdb=True,
        debug_sql=True,
    )
    if os.environ.get('TEST_WITH_REDSHIFT', None) == 'yes':
        test_runner.keepdb = True
    failures = test_runner.run_tests([
        'test_lookup',
        'test_or_lookups',
        'test_reverse_lookup',
        'test_string_lookup',
    ])
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
