import unittest

from django.db import connection, connections, router
from django.test import TestCase

from tests.app_postgresql.models import (
    ModelPostgreSQLA,
    ModelPostgreSQLB,
)


@unittest.skipUnless(
    ('db_postgresql' in connections and connections['db_postgresql'].vendor == 'postgresql' or
     'db_postgresql' in connections and connections['db_postgresql'].vendor == 'redshift'),
    'postgresql tests',
)
class RegexLookupPostgreSQLTest(TestCase):
    def setUp(self):
        super(RegexLookupPostgreSQLTest, self).setUp()

        ModelPostgreSQLA.objects.create(id=1, name='/blog/2017/05/07/kamakura_golden_week/')
        ModelPostgreSQLA.objects.create(id=2, name='/blog/2011/11/26/mount_box_net_on_ubuntu/')
        ModelPostgreSQLA.objects.create(id=3, name='I have hankaku space.')
        ModelPostgreSQLA.objects.create(id=4, name='abc\ndef\nf')
        ModelPostgreSQLA.objects.create(id=5, name='got\ttab')
        ModelPostgreSQLA.objects.create(id=6, name='hello\\sa')
        ModelPostgreSQLA.objects.create(id=7, name='/blog/')
        ModelPostgreSQLA.objects.create(id=8, name='test name')
        ModelPostgreSQLA.objects.create(id=9, name='test name1')

    def tearDown(self):
        super(RegexLookupPostgreSQLTest, self).tearDown()
        ModelPostgreSQLA.objects.all().delete()

    def test_regex(self):
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/1{1,2}?/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'/blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'abc\ndef\nf').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'got\ttab').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__regex=r'hello\\sa').count(),
        )

    def test_neregex(self):
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/1{1,2}?/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'/blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'abc\ndef\nf').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'got\ttab').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neregex=r'hello\\sa').count(),
        )
