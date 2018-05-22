============================
Django lookup extensions
============================

.. image:: https://travis-ci.org/uncovertruth/django-lookup-extensions.svg?branch=master
    :target: https://travis-ci.org/uncovertruth/django-lookup-extensions

.. image:: https://api.codacy.com/project/badge/Grade/d5a64517be0d49b6bf2f41c11df77730
    :target: https://www.codacy.com/app/develop_2/django-lookup-extensions?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=uncovertruth/django-lookup-extensions&amp;utm_campaign=Badge_Grade

.. image:: https://codebeat.co/badges/20da13a3-e873-412a-89b1-1a02bba47a23
    :target: https://codebeat.co/projects/github-com-uncovertruth-django-lookup-extensions-master

.. image:: https://www.codefactor.io/repository/github/uncovertruth/django-lookup-extensions/badge
    :target: https://www.codefactor.io/repository/github/uncovertruth/django-lookup-extensions

.. image:: https://codecov.io/gh/uncovertruth/django-lookup-extensions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/uncovertruth/django-lookup-extensions

.. image:: https://readthedocs.org/projects/django-lookup-extensions/badge/?version=latest
    :target: http://django-lookup-extensions.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/uncovertruth/django-lookup-extensions/shield.svg
    :target: https://pyup.io/repos/github/uncovertruth/django-lookup-extensions/
    :alt: Updates

.. image:: https://pyup.io/repos/github/uncovertruth/django-lookup-extensions/python-3-shield.svg
    :target: https://pyup.io/repos/github/uncovertruth/django-lookup-extensions/
    :alt: Python 3

.. .. image:: https://img.shields.io/pypi/v/django-lookup-extensions.svg
    :target: https://pypi.org/project/django-lookup-extensions

Django lookup extensions use **NOT** query.


* Free software: MIT license
* Documentation: https://django-lookup-extensions.readthedocs.io.


Installation
------------

To install Django lookup extensions, run this command in your terminal:

.. code-block:: console

    $ pip install django-lookup-extensions

This is the preferred method to install Django lookup extensions, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Usage
-----

Setup
^^^^^

Add **'lookup_extensions'** to your **INSTALLED_APPS** setting.:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'lookup_extensions',
        ...
    ]

AppConfig.ready imports lookups and register them using **django.db.models.fields.Field.register_lookup**.

Making queries
^^^^^^^^^^^^^^

Use lookup like Django standard lookups.

.. code-block:: python

    ModelA.objects.filter(name__neexact='test name')

Supported lookup types
----------------------

neexact is negate exact, neiexact is negate iexact, others are similar.

- neexact
- neiexact
- necontains
- neicontains
- nestartswith
- neendswith
- neistartswith
- neiendswith
- neregex
- neiregex

Extra regex lookup types
^^^^^^^^^^^^^^^^^^^^^^^^

These regex lookups support metacharacters **\\d**, **\\D**, **\w**, **\\W**, **\\s**, **\\S**.

MySQL, PostgreSQL and Redshift also support **\\<**, **\\>**.

Prefix follows the previous section.

- exregex
- exiregex
- neexregex
- neexiregex

Supported vendor types
----------------------

- MySQL
- PostgreSQL
- sqlite

  - lookups using `LIKE` aren't case sensitive.

    - necontains
    - nestartswith
    - neendswith

- Redshift

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
