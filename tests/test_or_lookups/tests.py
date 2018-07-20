from __future__ import unicode_literals

from operator import attrgetter
from unittest import skip

from django.db.models import Q

try:
    from or_lookups.models import Article
    from or_lookups.tests import OrLookupsTests as DjangoOrLookupsTests
except ImportError:
    print("Run tests/bootstrap.py before run tests.")
    raise


class OrLookupsTests(DjangoOrLookupsTests):
    def test_negate_filter_or(self):
        self.assertQuerysetEqual(
            (
                Article.objects.filter(headline__nestartswith='Hello') |
                Article.objects.filter(headline__nestartswith='Goodbye')
            ),
            [
                'Hello',
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline")
        )

        self.assertQuerysetEqual(
            Article.objects.filter(headline__necontains='Hello') | Article.objects.filter(headline__necontains='bye'),
            [
                'Hello',
                'Goodbye',
            ],
            attrgetter("headline")
        )

        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiexact='Hello') | Article.objects.filter(headline__necontains='ood'),
            [
                'Hello',
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline")
        )

        self.assertQuerysetEqual(
            Article.objects.filter(Q(headline__nestartswith='Hello') | Q(headline__nestartswith='Goodbye')),
            [
                'Hello',
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline")
        )

    def test_negate_stages(self):
        articles = Article.objects.all()
        self.assertQuerysetEqual(
            articles.filter(headline__nestartswith='Hello') & articles.filter(headline__nestartswith='Goodbye'),
            []
        )
        self.assertQuerysetEqual(
            articles.filter(headline__nestartswith='Hello') & articles.filter(headline__necontains='bye'),
            [],
            attrgetter("headline")
        )

    @skip("Support NOT IN filter")
    def test_negate_pk_in(self):
        self.assertQuerysetEqual(
            Article.objects.filter(pk__nein=[self.a1, self.a2, self.a3]), [
                'Hello',
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline"),
        )

        self.assertQuerysetEqual(
            Article.objects.filter(pk__nein=(self.a1, self.a2, self.a3)), [
                'Hello',
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline"),
        )

        self.assertQuerysetEqual(
            Article.objects.filter(pk__nein=[self.a1, self.a2, self.a3, 40000]), [
                'Hello',
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline"),
        )

    @skip("Support NOT IN filter")
    def test_negate_empty_in(self):
        # Passing "in" an empty list returns no results ...
        self.assertQuerysetEqual(
            Article.objects.filter(pk__nein=[]),
            []
        )
        # ... but can return results if we OR it with another query.
        self.assertQuerysetEqual(
            Article.objects.filter(Q(pk__nein=[]) | Q(headline__neicontains='goodbye')), [
                'Goodbye',
                'Hello and goodbye'
            ],
            attrgetter("headline"),
        )

    def test_negate_q_and(self):
        # Q arg objects are ANDed
        self.assertQuerysetEqual(
            Article.objects.filter(Q(headline__nestartswith='Hello'), Q(headline__necontains='bye')),
            [],
            attrgetter("headline")
        )
        # Q arg AND order is irrelevant
        self.assertQuerysetEqual(
            Article.objects.filter(Q(headline__necontains='bye'), headline__nestartswith='Hello'),
            [],
            attrgetter("headline"),
        )

        self.assertQuerysetEqual(
            Article.objects.filter(Q(headline__nestartswith='Hello') & Q(headline__nestartswith='Goodbye')),
            []
        )

    def test_negate_q_exclude(self):
        self.assertQuerysetEqual(
            Article.objects.exclude(Q(headline__nestartswith='Hello')),
            [
                'Hello',
                'Hello and goodbye',
            ],
            attrgetter("headline")
        )

    def test_negate_other_arg_queries(self):
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(Q(headline__nestartswith='Hello'), Q(headline__necontains='bye'))

        self.assertEqual(
            Article.objects.filter(Q(headline__nestartswith='Hello') | Q(headline__necontains='bye')).count(),
            2,
        )

        self.assertSequenceEqual(
            Article.objects.filter(Q(headline__nestartswith='Hello'), Q(headline__necontains='bye')).values(),
            [],
        )

        self.assertEqual(
            Article.objects.filter(Q(headline__nestartswith='Hello')).in_bulk([self.a1, self.a2]),
            {self.a2: Article.objects.get(pk=self.a2)}
        )
