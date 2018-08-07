from __future__ import unicode_literals

from datetime import datetime
from operator import attrgetter
from unittest import skip

from django.core.exceptions import FieldError
from django.db.models import (
    Exists,
    OuterRef,
)
from django.test import skipUnlessDBFeature

from utils import skipIfDBVendor

try:
    from lookup.models import (
        Article,
        Game,
        Player,
        Season,
        Tag,
    )
    from lookup.tests import LookupTests as DjangoLookupTests
except ImportError:
    print("Run tests/bootstrap.py before run tests.")
    raise


class LookupTests(DjangoLookupTests):
    def test_negate_lookup_int_as_str(self):
        self.assertQuerysetEqual(
            Article.objects.filter(id__neexact=str(self.a1.id)),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
            ],
        )

    @skipUnlessDBFeature('supports_date_lookup_using_string')
    def test_negate_lookup_date_as_str(self):
        self.assertQuerysetEqual(
            Article.objects.filter(pub_date__nestartswith='2005'),
            []
        )

    def test_negate_iterator(self):
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neendswith='4').iterator(),
            [
                'Article 5',
                'Article 6',
                'Article 2',
                'Article 3',
                'Article 7',
                'Article 1',
            ],
            transform=attrgetter('headline'),
        )

    def test_negate_count(self):
        self.assertEqual(Article.objects.filter(pub_date__neexact=datetime(2005, 7, 27)).count(), 4)
        self.assertEqual(Article.objects.filter(headline__nestartswith='Blah blah').count(), 7)
        self.assertEqual(Article.objects.filter(pub_date__neexact='2005-07-27 00:00:00').count(), 4)

    def test_values(self):
        self.assertSequenceEqual(
            Article.objects.filter(pub_date__neexact=datetime(2005, 7, 27)).values('id'),
            [
                {'id': self.a5.id},
                {'id': self.a6.id},
                {'id': self.a4.id},
                {'id': self.a1.id},
            ],
        )

    def test_negate_get_next_previous_by(self):
        self.assertEqual(
            repr(self.a2.get_next_by_pub_date(headline__neendswith='6')),
            '<Article: Article 3>',
        )

    def test_negate_escaping(self):
        Article.objects.create(headline='Article_ with underscore', pub_date=datetime(2005, 11, 20))

        self.assertQuerysetEqual(
            Article.objects.filter(headline__nestartswith='Article'),
            [],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__nestartswith='Article_'),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )
        Article.objects.create(headline='Article% with percent sign', pub_date=datetime(2005, 11, 21))
        self.assertQuerysetEqual(
            Article.objects.filter(headline__nestartswith='Article'),
            []
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__nestartswith='Article%'),
            [
                '<Article: Article_ with underscore>',
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ]
        )
        Article.objects.create(headline='Article with \\ backslash', pub_date=datetime(2005, 11, 22))
        self.assertQuerysetEqual(
            Article.objects.filter(headline__necontains='\\'),
            [
                '<Article: Article% with percent sign>',
                '<Article: Article_ with underscore>',
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )

    def test_negate_exclude(self):
        Article.objects.create(headline='Article_ with underscore', pub_date=datetime(2005, 11, 20))
        Article.objects.create(headline='Article% with percent sign', pub_date=datetime(2005, 11, 21))
        Article.objects.create(headline='Article with \\ backslash', pub_date=datetime(2005, 11, 22))

        self.assertQuerysetEqual(
            Article.objects.filter(headline__necontains='Article').exclude(headline__necontains='with'),
            []
        )
        self.assertQuerysetEqual(
            Article.objects.exclude(headline__nestartswith="Article_"),
            [
                '<Article: Article_ with underscore>',
            ]
        )

    def test_negate_none(self):
        self.assertQuerysetEqual(Article.objects.none().filter(headline__nestartswith='Article'), [])
        self.assertQuerysetEqual(Article.objects.filter(headline__nestartswith='Article').none(), [])

    @skip("Support NOT IN filter")
    def test_negate_in(self):
        # using __in with an empty list should return an empty query set
        self.assertQuerysetEqual(
            Article.objects.filter(id__nein=[]),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.exclude(id__nein=[]),
            [],
        )

    @skip("Support NOT IN filter")
    def test_negate_in_different_database(self):
        with self.assertRaisesMessage(
            ValueError,
            "Subqueries aren't allowed across different databases. Force the "
            "inner query to be evaluated using `list(inner_query)`."
        ):
            list(Article.objects.filter(id__nein=Article.objects.using('other').all()))

    def test_negate_regex(self):
        # Create some articles with a bit more interesting headlines for testing field lookups:
        for a in Article.objects.all():
            a.delete()
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='f')
        Article.objects.create(pub_date=now, headline='fo')
        Article.objects.create(pub_date=now, headline='foo')
        Article.objects.create(pub_date=now, headline='fooo')
        Article.objects.create(pub_date=now, headline='hey-Foo')
        Article.objects.create(pub_date=now, headline='bar')
        Article.objects.create(pub_date=now, headline='AbBa')
        Article.objects.create(pub_date=now, headline='baz')
        Article.objects.create(pub_date=now, headline='baxZ')
        # zero-or-more
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'fo*'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiregex=r'fo*'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
            ],
        )
        # one-or-more
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'fo+'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: hey-Foo>'
            ],
        )
        # wildcard
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'fooo?'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: hey-Foo>',
            ],
        )
        # leading anchor
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'^b'),
            [
                '<Article: AbBa>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiregex=r'^a'),
            [
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        # trailing anchor
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'z$'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiregex=r'z$'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>'
            ]
        )
        # character sets
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'ba[rz]'),
            [
                '<Article: AbBa>',
                '<Article: baxZ>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>'
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'ba.[RxZ]'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiregex=r'ba[RxZ]'),
            [
                '<Article: AbBa>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )

        # and more articles:
        Article.objects.create(pub_date=now, headline='foobar')
        Article.objects.create(pub_date=now, headline='foobaz')
        Article.objects.create(pub_date=now, headline='ooF')
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='zoocarfaz')
        Article.objects.create(pub_date=now, headline='barfoobaz')
        Article.objects.create(pub_date=now, headline='bazbaRFOO')

        # alternation
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'oo(f|b)'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiregex=r'oo(f|b)'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: zoocarfaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'^foo(f|b)'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: barfoobaz>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',

            ],
        )

        # greedy matching
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'b.*az'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: foobar>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neiregex=r'b.*ar'),
            [
                '<Article: AbBa>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: foobaz>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
            ]
        )

    @skipUnlessDBFeature('supports_regex_backreferencing')
    def test_negate_regex_backreferencing(self):
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobar')
        Article.objects.create(pub_date=now, headline='foobaz')
        Article.objects.create(pub_date=now, headline='ooF')
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='zoocarfaz')
        Article.objects.create(pub_date=now, headline='barfoobaz')
        Article.objects.create(pub_date=now, headline='bazbaRFOO')
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neregex=r'b(.).*b\1'),
            [
                '<Article: foobar>',
                '<Article: foobaz>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )

    @skipIfDBVendor('postgresql', 'mysql')
    def test_negate_regex_null_sqlite(self):
        Season.objects.create(year=2012, gt=None)
        self.assertQuerysetEqual(
            Season.objects.filter(gt__neregex=r'^$'),
            [
                '<Season: 2012>',
            ],
        )

    @skipIfDBVendor('sqlite')
    def test_negate_regex_null_without_sqlite(self):
        Season.objects.create(year=2012, gt=None)
        self.assertQuerysetEqual(
            Season.objects.filter(gt__neregex=r'^$'),
            [],
        )

    def test_negate_regex_non_string(self):
        Season.objects.create(year=2013, gt=444)
        self.assertQuerysetEqual(
            Season.objects.filter(gt__neregex=r'^444$'),
            [],
        )

    def test_negate_regex_non_ascii(self):
        Player.objects.create(name='\u2660')
        with self.assertRaises(Player.DoesNotExist):
            Player.objects.get(name__neregex='\u2660')

    def test_negate_nonfield_lookups(self):
        msg = "Unsupported lookup 'blahblah' for CharField or join on the field not permitted."
        with self.assertRaisesMessage(FieldError, msg):
            Article.objects.filter(headline__blahblah__neexact=99)

    @skip("Support NOT IN filter")
    def test_negate_lookup_collision(self):
        # 'gt' is used as a code number for the year, e.g. 111=>2009.
        season_2009 = Season.objects.create(year=2009, gt=111)
        season_2009.games.create(home="Houston Astros", away="St. Louis Cardinals")
        season_2010 = Season.objects.create(year=2010, gt=222)
        season_2010.games.create(home="Houston Astros", away="Chicago Cubs")
        season_2010.games.create(home="Houston Astros", away="Milwaukee Brewers")
        season_2010.games.create(home="Houston Astros", away="St. Louis Cardinals")
        season_2011 = Season.objects.create(year=2011, gt=333)
        season_2011.games.create(home="Houston Astros", away="St. Louis Cardinals")
        season_2011.games.create(home="Houston Astros", away="Milwaukee Brewers")
        hunter_pence = Player.objects.create(name="Hunter Pence")
        hunter_pence.games.set(Game.objects.filter(season__year__in=[2009, 2010]))
        pudge = Player.objects.create(name="Ivan Rodriquez")
        pudge.games.set(Game.objects.filter(season__year=2009))
        pedro_feliz = Player.objects.create(name="Pedro Feliz")
        pedro_feliz.games.set(Game.objects.filter(season__year__in=[2011]))
        johnson = Player.objects.create(name="Johnson")
        johnson.games.set(Game.objects.filter(season__year__in=[2011]))

        # Games in 2010
        self.assertEqual(Game.objects.filter(season__year__exact=2010).count(), 3)
        self.assertEqual(Game.objects.filter(season__gt__exact=222).count(), 3)

        # Games in 2011
        self.assertEqual(Game.objects.filter(season__year__exact=2011).count(), 2)
        self.assertEqual(Game.objects.filter(season__gt__exact=333).count(), 2)

        # Games played in 2010 and 2011
        self.assertEqual(Game.objects.filter(season__year__in=[2010, 2011]).count(), 5)
        self.assertEqual(Game.objects.filter(season__gt__in=[222, 333]).count(), 5)

        # Players who played in 2009
        self.assertEqual(Player.objects.filter(games__season__year__exact=2009).distinct().count(), 2)
        self.assertEqual(Player.objects.filter(games__season__gt__exact=111).distinct().count(), 2)

        # Players who played in 2010
        self.assertEqual(Player.objects.filter(games__season__year__exact=2010).distinct().count(), 1)
        self.assertEqual(Player.objects.filter(games__season__gt__exact=222).distinct().count(), 1)

        # Players who played in 2011
        self.assertEqual(Player.objects.filter(games__season__year__exact=2011).distinct().count(), 2)

    @skip("Support IS NOT NULL filter")
    def test_negate_exact_none_transform(self):
        """Transforms are used for __neexact=None."""
        Season.objects.create(year=1, nulled_text_field='not null')
        self.assertFalse(Season.objects.filter(nulled_text_field__neisnull=True))
        self.assertTrue(Season.objects.filter(nulled_text_field__nulled__neisnull=True))
        self.assertTrue(Season.objects.filter(nulled_text_field__nulled__neexact=None))

    @skip("Support IS NOT NULL filter")
    def test_negate_custom_field_none_rhs(self):
        """
        __neexact=value is transformed to __neisnull=True if Field.get_prep_value()
        converts value to None.
        """
        season = Season.objects.create(year=2012, nulled_text_field=None)
        self.assertTrue(Season.objects.filter(pk=season.pk, nulled_text_field__neisnull=True))

    def test_exregex(self):
        """Copy from test_exregex."""
        # Create some articles with a bit more interesting headlines for testing field lookups:
        for a in Article.objects.all():
            a.delete()
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='f')
        Article.objects.create(pub_date=now, headline='fo')
        Article.objects.create(pub_date=now, headline='foo')
        Article.objects.create(pub_date=now, headline='fooo')
        Article.objects.create(pub_date=now, headline='hey-Foo')
        Article.objects.create(pub_date=now, headline='bar')
        Article.objects.create(pub_date=now, headline='AbBa')
        Article.objects.create(pub_date=now, headline='baz')
        Article.objects.create(pub_date=now, headline='baxZ')
        # zero-or-more
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'fo*'),
            ['<Article: f>', '<Article: fo>', '<Article: foo>', '<Article: fooo>']
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exiregex=r'fo*'),
            [
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ]
        )
        # one-or-more
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'fo+'),
            ['<Article: fo>', '<Article: foo>', '<Article: fooo>']
        )
        # wildcard
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'fooo?'),
            ['<Article: foo>', '<Article: fooo>']
        )
        # leading anchor
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'^b'),
            ['<Article: bar>', '<Article: baxZ>', '<Article: baz>']
        )
        self.assertQuerysetEqual(Article.objects.filter(headline__exiregex=r'^a'), ['<Article: AbBa>'])
        # trailing anchor
        self.assertQuerysetEqual(Article.objects.filter(headline__exregex=r'z$'), ['<Article: baz>'])
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exiregex=r'z$'),
            ['<Article: baxZ>', '<Article: baz>']
        )
        # character sets
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'ba[rz]'),
            ['<Article: bar>', '<Article: baz>']
        )
        self.assertQuerysetEqual(Article.objects.filter(headline__exregex=r'ba.[RxZ]'), ['<Article: baxZ>'])
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exiregex=r'ba[RxZ]'),
            ['<Article: bar>', '<Article: baxZ>', '<Article: baz>']
        )

        # and more articles:
        Article.objects.create(pub_date=now, headline='foobar')
        Article.objects.create(pub_date=now, headline='foobaz')
        Article.objects.create(pub_date=now, headline='ooF')
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='zoocarfaz')
        Article.objects.create(pub_date=now, headline='barfoobaz')
        Article.objects.create(pub_date=now, headline='bazbaRFOO')

        # alternation
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'oo(f|b)'),
            [
                '<Article: barfoobaz>',
                '<Article: foobar>',
                '<Article: foobarbaz>',
                '<Article: foobaz>',
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exiregex=r'oo(f|b)'),
            [
                '<Article: barfoobaz>',
                '<Article: foobar>',
                '<Article: foobarbaz>',
                '<Article: foobaz>',
                '<Article: ooF>',
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'^foo(f|b)'),
            ['<Article: foobar>', '<Article: foobarbaz>', '<Article: foobaz>']
        )

        # greedy matching
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'b.*az'),
            [
                '<Article: barfoobaz>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: foobarbaz>',
                '<Article: foobaz>',
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exiregex=r'b.*ar'),
            [
                '<Article: bar>',
                '<Article: barfoobaz>',
                '<Article: bazbaRFOO>',
                '<Article: foobar>',
                '<Article: foobarbaz>',
            ]
        )

    @skipUnlessDBFeature('supports_exregex_backreferencing')
    def test_exregex_backreferencing(self):
        """Copy from test_regex_backreferencing."""
        # grouping and backreferences
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobar')
        Article.objects.create(pub_date=now, headline='foobaz')
        Article.objects.create(pub_date=now, headline='ooF')
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='zoocarfaz')
        Article.objects.create(pub_date=now, headline='barfoobaz')
        Article.objects.create(pub_date=now, headline='bazbaRFOO')
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'b(.).*b\1'),
            ['<Article: barfoobaz>', '<Article: bazbaRFOO>', '<Article: foobarbaz>']
        )

    def test_exregex_null(self):
        """Copy from test_regex_null.

        A exregex lookup does not fail on null/None values
        """
        Season.objects.create(year=2012, gt=None)
        self.assertQuerysetEqual(Season.objects.filter(gt__exregex=r'^$'), [])

    def test_exregex_non_string(self):
        """Copy from test_regex_non_string.

        A exregex lookup does not fail on non-string fields
        """
        Season.objects.create(year=2013, gt=444)
        self.assertQuerysetEqual(Season.objects.filter(gt__exregex=r'^444$'), ['<Season: 2013>'])

    def test_exregex_non_ascii(self):
        """Copy from test_regex_non_ascii.

        A exregex lookup does not trip on non-ASCII characters.
        """
        Player.objects.create(name='\u2660')
        Player.objects.get(name__exregex='\u2660')

    def test_negate_exregex(self):
        """Copy from test_negate_regex."""
        # Create some articles with a bit more interesting headlines for testing field lookups:
        for a in Article.objects.all():
            a.delete()
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='f')
        Article.objects.create(pub_date=now, headline='fo')
        Article.objects.create(pub_date=now, headline='foo')
        Article.objects.create(pub_date=now, headline='fooo')
        Article.objects.create(pub_date=now, headline='hey-Foo')
        Article.objects.create(pub_date=now, headline='bar')
        Article.objects.create(pub_date=now, headline='AbBa')
        Article.objects.create(pub_date=now, headline='baz')
        Article.objects.create(pub_date=now, headline='baxZ')
        # zero-or-more
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'fo*'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'fo*'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
            ],
        )
        # one-or-more
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'fo+'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: hey-Foo>'
            ],
        )
        # wildcard
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'fooo?'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: hey-Foo>',
            ],
        )
        # leading anchor
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'^b'),
            [
                '<Article: AbBa>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'^a'),
            [
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        # trailing anchor
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'z$'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'z$'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>'
            ]
        )
        # character sets
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'ba[rz]'),
            [
                '<Article: AbBa>',
                '<Article: baxZ>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>'
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'ba.[RxZ]'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'ba[RxZ]'),
            [
                '<Article: AbBa>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
            ],
        )

        # and more articles:
        Article.objects.create(pub_date=now, headline='foobar')
        Article.objects.create(pub_date=now, headline='foobaz')
        Article.objects.create(pub_date=now, headline='ooF')
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='zoocarfaz')
        Article.objects.create(pub_date=now, headline='barfoobaz')
        Article.objects.create(pub_date=now, headline='bazbaRFOO')

        # alternation
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'oo(f|b)'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'oo(f|b)'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: zoocarfaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'^foo(f|b)'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: barfoobaz>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: bazbaRFOO>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',

            ],
        )

        # greedy matching
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'b.*az'),
            [
                '<Article: AbBa>',
                '<Article: bar>',
                '<Article: baxZ>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: foobar>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
            ]
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'b.*ar'),
            [
                '<Article: AbBa>',
                '<Article: baxZ>',
                '<Article: baz>',
                '<Article: f>',
                '<Article: fo>',
                '<Article: foo>',
                '<Article: foobaz>',
                '<Article: fooo>',
                '<Article: hey-Foo>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
            ]
        )

    @skipUnlessDBFeature('supports_exregex_backreferencing')
    def test_negate_exregex_backreferencing(self):
        """Copy from test_negate_regex_backreferencing."""
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobar')
        Article.objects.create(pub_date=now, headline='foobaz')
        Article.objects.create(pub_date=now, headline='ooF')
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='zoocarfaz')
        Article.objects.create(pub_date=now, headline='barfoobaz')
        Article.objects.create(pub_date=now, headline='bazbaRFOO')
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'b(.).*b\1'),
            [
                '<Article: foobar>',
                '<Article: foobaz>',
                '<Article: ooF>',
                '<Article: zoocarfaz>',
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )

    @skipIfDBVendor('postgresql', 'mysql')
    def test_negate_exregex_null_sqlite(self):
        """Copy from test_negate_regex_null_sqlite."""
        Season.objects.create(year=2012, gt=None)
        self.assertQuerysetEqual(
            Season.objects.filter(gt__neexregex=r'^$'),
            [
                '<Season: 2012>',
            ],
        )

    @skipIfDBVendor('sqlite')
    def test_negate_exregex_null_without_sqlite(self):
        """Copy from test_negate_regex_null_without_sqlite."""
        Season.objects.create(year=2012, gt=None)
        self.assertQuerysetEqual(
            Season.objects.filter(gt__neexregex=r'^$'),
            [],
        )

    def test_negate_exregex_non_string(self):
        """Copy from test_negate_regex_non_string."""
        Season.objects.create(year=2013, gt=444)
        self.assertQuerysetEqual(
            Season.objects.filter(gt__neexregex=r'^444$'),
            [],
        )

    def test_negate_exregex_non_ascii(self):
        """Copy from test_negate_regex_non_ascii."""
        Player.objects.create(name='\u2660')
        with self.assertRaises(Player.DoesNotExist):
            Player.objects.get(name__neexregex='\u2660')

    @skipIfDBVendor('sqlite')
    def test_exregex_word_starts_or_ends_brackets(self):
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='foo barbaz')
        Article.objects.create(pub_date=now, headline='Foo Barbaz')
        Article.objects.create(pub_date=now, headline='foobar baz')
        Article.objects.create(pub_date=now, headline='FooBar baz')
        Article.objects.create(pub_date=now, headline='foo bar baz')
        Article.objects.create(pub_date=now, headline='Foo Bar Baz')

        # [[:<:]] [[:>:]]
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'\<Bar\>'),
            [
                '<Article: Foo Bar Baz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exiregex=r'\<bar\>').order_by('id'),
            [
                '<Article: foo bar baz>',
                '<Article: Foo Bar Baz>',
            ],
        )

    @skipIfDBVendor('sqlite')
    def test_negate_exregex_word_starts_or_ends_brackets(self):
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobarbaz')
        Article.objects.create(pub_date=now, headline='foo barbaz')
        Article.objects.create(pub_date=now, headline='Foo Barbaz')
        Article.objects.create(pub_date=now, headline='foobar baz')
        Article.objects.create(pub_date=now, headline='FooBar baz')
        Article.objects.create(pub_date=now, headline='foo bar baz')
        Article.objects.create(pub_date=now, headline='Foo Bar Baz')

        # [[:<:]] [[:>:]]
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'\<Bar\>')
                           .exclude(headline__exregex=r'\<Article\>')
                           .order_by('id'),
            [
                '<Article: foobarbaz>',
                '<Article: foo barbaz>',
                '<Article: Foo Barbaz>',
                '<Article: foobar baz>',
                '<Article: FooBar baz>',
                '<Article: foo bar baz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexiregex=r'\<bar\>')
                           .exclude(headline__exregex=r'\<Article\>')
                           .order_by('id'),
            [
                '<Article: foobarbaz>',
                '<Article: foo barbaz>',
                '<Article: Foo Barbaz>',
                '<Article: foobar baz>',
                '<Article: FooBar baz>',
            ]
        )

    def test_exregex_short_end_escapes(self):
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobarbaz')

        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'\w+\s\d'),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'\W'),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'^\D+$'),
            [
                '<Article: foobarbaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__exregex=r'^\S+$'),
            [
                '<Article: foobarbaz>',
            ],
        )

    def test_negate_exregex_short_end_escapes(self):
        now = datetime.now()
        Article.objects.create(pub_date=now, headline='foobarbaz')

        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'\w+\s\d'),
            [
                '<Article: foobarbaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'\W'),
            [
                '<Article: foobarbaz>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'^\D+$'),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )
        self.assertQuerysetEqual(
            Article.objects.filter(headline__neexregex=r'^\S+$'),
            [
                '<Article: Article 5>',
                '<Article: Article 6>',
                '<Article: Article 4>',
                '<Article: Article 2>',
                '<Article: Article 3>',
                '<Article: Article 7>',
                '<Article: Article 1>',
            ],
        )

    def test_complement(self):
        tags = Tag.objects.filter(articles=OuterRef('id'), name='Tag 2')
        self.assertQuerysetEqual(
            Article.objects.filter(tag__complement=Exists(tags)).filter(author=self.au1),
            [
                '<Article: Article 4>',
                '<Article: Article 3>',
            ],
        )

    def test_negate_complement(self):
        tags = Tag.objects.filter(articles=OuterRef('id'), name='Tag 2')
        self.assertQuerysetEqual(
            Article.objects.filter(tag__complement=~Exists(tags)).filter(author=self.au1),
            [
                '<Article: Article 2>',
                '<Article: Article 1>',
            ],
        )
