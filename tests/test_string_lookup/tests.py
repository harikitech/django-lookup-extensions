from __future__ import unicode_literals

try:
    from string_lookup.models import Article, Foo
    from string_lookup.tests import StringLookupTests as DjangoStringLookupTests
except ImportError:
    raise


class StringLookupTests(DjangoStringLookupTests):
    def test_negate_unicode_chars_in_queries(self):
        fx = Foo(name='Bjorn', friend='CHANGED')
        fx.save()
        self.assertEqual(Foo.objects.get(friend__necontains='\xe7'), fx)

    def test_negate_queries_on_textfields(self):
        a = Article(name='Test', text='CHANGED')
        a.save()
        self.assertEqual(Article.objects.get(text__neexact='The quick brown fox jumps over the lazy dog.'), a)

        self.assertEqual(Article.objects.get(text__necontains='quick brown fox'), a)

    def test_negate_ipaddress_on_postgresql(self):
        a = Article(name='IP test', text='The body', submitted_from='192.0.1.100')  # CHANGED
        a.save()
        self.assertSequenceEqual(Article.objects.filter(submitted_from__necontains='192.0.2'), [a])
        self.assertEqual(Article.objects.filter(submitted_from__necontains='32').count(), 1)
