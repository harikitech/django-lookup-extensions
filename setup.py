#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

import inverse_lookup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: Put package requirements here
]

setup_requirements = [
    # TODO(uncovertruth): Put setup requirements here
]

test_requirements = [
    # TODO: Put package test requirements here
]

setup(
    name='django-inverse-lookup',
    version=inverse_lookup.__version__,
    description="Django inverse lookup use NOT query.",
    long_description=readme + '\n\n' + history,
    author=inverse_lookup.__author__,
    author_email=inverse_lookup.__email__,
    url='https://github.com/uncovertruth/django-inverse-lookup',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='django, inverse lookup, filter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
