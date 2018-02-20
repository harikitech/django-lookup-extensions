#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import sys

from django.test.runner import setup_databases


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tests.test_settings')


def runtests():
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    django.setup()

    if hasattr(django, 'setup'):
        django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)
    # test_runner.setup_databases()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
