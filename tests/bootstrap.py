#!/usr/bin/env python

import logging
import os

import django
from django.utils.six.moves.urllib import request
from django.utils.six.moves.urllib.error import HTTPError

logger = logging.getLogger()


DJANGO_VERSION = django.get_version()
if 'dev' in DJANGO_VERSION:
    DJANGO_VERSION = 'master'
DJANGO_TEST_APP_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'vendor',
    'django',
    DJANGO_VERSION,
    'tests',
)
DJANGO_TEST_DOWNLOAD_URL = 'https://raw.githubusercontent.com/django/django/{version}/tests/{test_app}/{test_file}'
DJANGO_LOOKUP_TEST_APP_FILES = {
    'lookup': [
        'test_decimalfield.py',
        'test_lookups.py',
        'test_timefield.py',
    ],
    'or_lookups': [],
    'reverse_lookup': [],
    'string_lookup': [],
}


def download_django_test_apps():
    def _download_file(test_app, test_file):
        download_url = DJANGO_TEST_DOWNLOAD_URL.format(
            version=DJANGO_VERSION,
            test_app=test_app,
            test_file=test_file,
        )
        to_dir = os.path.join(
            DJANGO_TEST_APP_PATH,
            test_app,
        )
        if not os.path.isdir(to_dir):
            os.makedirs(to_dir)
        to_file = os.path.join(
            to_dir,
            test_file,
        )
        if not os.path.isfile(to_file):
            try:
                with open(to_file, 'wb') as fp:
                    res = request.urlopen(download_url)
                    fp.write(res.read())
                    logger.info("Download: %s", download_url)
                    res.close()
            except HTTPError:
                logger.warn("Not found: %s", download_url)

    for test_app, test_files in DJANGO_LOOKUP_TEST_APP_FILES.items():
        _download_file(test_app, '__init__.py')
        _download_file(test_app, 'models.py')
        _download_file(test_app, 'tests.py')
        for test_file in test_files:
            _download_file(test_app, test_file)


if __name__ == "__main__":
    download_django_test_apps()
