=====
Usage
=====

To use Django lookup extensions in a project::

    import lookup_extensions

Exists and Not exists
=====================

.. code-block:: python

    from django.db.models import Exists, OuterRef

    tags = Tag.objects.filter(articles=OuterRef('id'), name='Tag 2')
    Article.objects.filter(tag__exists=Exists(tags)).filter(author=self.au1)
