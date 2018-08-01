=====
Usage
=====

Set extended manager to your models
-----------------------------------

.. code-block:: python

    from lookup_extensions.manager import Manager

    class Article(models.Model):
        # ...

        objects = Manager()

Exists and Not exists
---------------------

.. code-block:: python

    from django.db.models import Exists, OuterRef

    tags = Tag.objects.filter(articles=OuterRef('id'), name='Tag 2')
    Article.objects.filter(tag__exists=Exists(tags)).filter(author=self.au1)
