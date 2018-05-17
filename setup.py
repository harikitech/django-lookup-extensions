#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import (
    find_packages,
    setup,
)

import lookup_extensions

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Django>=1.11',
]

test_requirements = [
    # TODO: Put package test requirements here
]

setup(
    name='django-lookup-extensions',
    version=lookup_extensions.__version__,
    description="Django lookup extensions use NOT query.",
    long_description=readme + '\n\n' + history,
    author=lookup_extensions.__author__,
    author_email=lookup_extensions.__email__,
    url='https://github.com/uncovertruth/django-lookup-extensions',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='django, lookup extensions, filter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='runtests.runtests',
    tests_require=test_requirements,
)
