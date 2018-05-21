import unittest

from django.db import connections
from django.test import TestCase

from tests.app_default.models import ModelA
from tests.app_mysql.models import ModelMySQLA
from tests.app_postgresql.models import ModelPostgreSQLA


@unittest.skipUnless(
    ('default' in connections and connections['default'].vendor == 'sqlite'),
    'sqlite tests',
)
class ExRegexLookupSqliteTest(TestCase):
    def setUp(self):
        super(ExRegexLookupSqliteTest, self).setUp()

        ModelA.objects.create(id=1, name='/blog/2017/05/07/kamakura_golden_week/')
        ModelA.objects.create(id=2, name='/blog/2011/11/26/mount_box_net_on_ubuntu/')
        ModelA.objects.create(id=3, name='I have hankaku space.')
        ModelA.objects.create(id=4, name=r'abc\ndef\nf')
        ModelA.objects.create(id=5, name=r'got\ttab')
        ModelA.objects.create(id=6, name='hello a')
        ModelA.objects.create(id=7, name='/blog/')
        ModelA.objects.create(id=8, name='test name')
        ModelA.objects.create(id=9, name='test name1')

    def tearDown(self):
        super(ExRegexLookupSqliteTest, self).tearDown()
        ModelA.objects.all().delete()

    def test_exregex(self):
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex='/blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'abc\\ndef\\nf').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'got\\ttab').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'hello\s+a').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exregex=r'I \w').count(),
        )
        # case sensitive
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exregex=r'i \w').count(),
        )

    def test_exregex_unsupported(self):
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exregex=r'\<hankaku').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exregex=r'\<ankaku').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exregex=r'hankaku\>').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exregex=r'hankak\>').count(),
        )

    def test_exiregex(self):
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'i HAVE\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'/Blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'^/Blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex='/Blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'Abc\\nDef\\nf').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'Got\\tTab').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'Hello\s+a').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__exiregex=r'i \w').count(),
        )

    def test_exiregex_unsupported(self):
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exiregex=r'\<Hankaku').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exiregex=r'\<Ankaku').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exiregex=r'Hankaku\>').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exiregex=r'Hankak\>').count(),
        )

    def test_exregex_sql_injection(self):
        self.assertEqual(
            0,
            ModelA.objects.filter(name__exregex="' or 'A'='A").count(),
        )

    def test_neexregex(self):
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex='/blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'abc\\ndef\\nf').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'got\\ttab').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'hello\s+a').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexregex=r'I \w').count(),
        )
        #  {1,2}? errors (1139, "Got error 'repetition-operator operand invalid' from regexp")

    def test_neexregex_unsupported(self):
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexregex=r'\<hankaku').count(),
        )
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexregex=r'\<ankaku').count(),
        )
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexregex=r'hankaku\>').count(),
        )
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexregex=r'hankak\>').count(),
        )

    def test_neexiregex(self):
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'i HAVE\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'^/Blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex='/Blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'Abc\\nDef\\nf').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'Got\\tTab').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'Hello\s+a').count(),
        )
        self.assertEqual(
            8,
            ModelA.objects.filter(name__neexiregex=r'i \w').count(),
        )

    def test_neexiregex_unsupported(self):
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexiregex=r'\<Hankaku').count(),
        )
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexiregex=r'\<Ankaku').count(),
        )
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexiregex=r'Hankaku\>').count(),
        )
        self.assertEqual(
            9,
            ModelA.objects.filter(name__neexiregex=r'Hankak\>').count(),
        )


@unittest.skipUnless(
    ('db_mysql' in connections and connections['db_mysql'].vendor == 'mysql'),
    'mysql tests',
)
class ExRegexLookupMySQLTest(TestCase):
    def setUp(self):
        super(ExRegexLookupMySQLTest, self).setUp()

        ModelMySQLA.objects.create(id=1, name='/blog/2017/05/07/kamakura_golden_week/')
        ModelMySQLA.objects.create(id=2, name='/blog/2011/11/26/mount_box_net_on_ubuntu/')
        ModelMySQLA.objects.create(id=3, name='I have hankaku space.')
        ModelMySQLA.objects.create(id=4, name=r'abc\ndef\nf')
        ModelMySQLA.objects.create(id=5, name=r'got\ttab')
        ModelMySQLA.objects.create(id=6, name='hello a')
        ModelMySQLA.objects.create(id=7, name='/blog/')
        ModelMySQLA.objects.create(id=8, name='test name')
        ModelMySQLA.objects.create(id=9, name='test name1')

    def tearDown(self):
        super(ExRegexLookupMySQLTest, self).tearDown()
        ModelMySQLA.objects.all().delete()

    def test_exregex(self):
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex='/blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'abc\\ndef\\nf').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'got\\ttab').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'hello\s+a').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'\<hankaku').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__exregex=r'\<ankaku').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'hankaku\>').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__exregex=r'hankak\>').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exregex=r'I \w').count(),
        )
        # case sensitive
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__exregex=r'i \w').count(),
        )

    def test_iregex(self):
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'i HAVE\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'^/Blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex='/Blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'Abc\\nDef\\nf').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'Got\\tTab').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'Hello\s+a').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'\<Hankaku').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__exiregex=r'\<Ankaku').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'Hankaku\>').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__exiregex=r'Hankak\>').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__exiregex=r'i \w').count(),
        )

    def test_exregex_sql_injection(self):
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__exregex="' or 'A'='A").count(),
        )

    def test_neexregex(self):
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex='/blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'abc\\ndef\\nf').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'got\\ttab').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'hello\s+a').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'\<hankaku').count(),
        )
        self.assertEqual(
            9,
            ModelMySQLA.objects.filter(name__neexregex=r'\<ankaku').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'hankaku\>').count(),
        )
        self.assertEqual(
            9,
            ModelMySQLA.objects.filter(name__neexregex=r'hankak\>').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexregex=r'I \w').count(),
        )
        #  {1,2}? errors (1139, "Got error 'repetition-operator operand invalid' from regexp")

    def test_neexiregex(self):
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'i HAVE\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'^/Blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex='/Blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'Abc\\nDef\\nf').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'Got\\tTab').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'Hello\s+a').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'\<Hankaku').count(),
        )
        self.assertEqual(
            9,
            ModelMySQLA.objects.filter(name__neexiregex=r'\<Ankaku').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'Hankaku\>').count(),
        )
        self.assertEqual(
            9,
            ModelMySQLA.objects.filter(name__neexiregex=r'Hankak\>').count(),
        )
        self.assertEqual(
            8,
            ModelMySQLA.objects.filter(name__neexiregex=r'i \w').count(),
        )


@unittest.skipUnless(
    ('db_postgresql' in connections and connections['db_postgresql'].vendor == 'postgresql' or
     'db_postgresql' in connections and connections['db_postgresql'].vendor == 'redshift'),
    'postgresql tests',
)
class RegexLookupPostgreSQLRedshiftTest(TestCase):
    def setUp(self):
        super(RegexLookupPostgreSQLRedshiftTest, self).setUp()

        ModelPostgreSQLA.objects.create(id=1, name='/blog/2017/05/07/kamakura_golden_week/')
        ModelPostgreSQLA.objects.create(id=2, name='/blog/2011/11/26/mount_box_net_on_ubuntu/')
        ModelPostgreSQLA.objects.create(id=3, name='I have hankaku space.')
        ModelPostgreSQLA.objects.create(id=4, name=r'abc\ndef\nf')
        ModelPostgreSQLA.objects.create(id=5, name=r'got\ttab')
        ModelPostgreSQLA.objects.create(id=6, name='hello a')
        ModelPostgreSQLA.objects.create(id=7, name='/blog/')
        ModelPostgreSQLA.objects.create(id=8, name='test name')
        ModelPostgreSQLA.objects.create(id=9, name='test name1')

    def tearDown(self):
        super(RegexLookupPostgreSQLRedshiftTest, self).tearDown()
        ModelPostgreSQLA.objects.all().delete()

    def test_exregex(self):
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex='/blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'abc\\ndef\\nf').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'got\\ttab').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'hello\s+a').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'\<hankaku').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__exregex=r'\<ankaku').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'hankaku\>').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__exregex=r'hankak\>').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'I \w').count(),
        )

    def test_iregex(self):
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'i HAVE\shankaku space.').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'^/Blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex='/Blog/$').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'Abc\\nDef\\nf').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'Got\\tTab').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'Hello\s+a').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'\<Hankaku').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'\<Ankaku').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'Hankaku\>').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'Hankak\>').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'i \w').count(),
        )

    def test_exregex_sql_injection(self):
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__exregex="' or 'A'='A").count(),
        )

    def test_neexregex(self):
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'I have\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'^/blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex='/blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'abc\\ndef\\nf').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'got\\ttab').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'hello\s+a').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'\<hankaku').count(),
        )
        self.assertEqual(
            9,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'\<ankaku').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'hankaku\>').count(),
        )
        self.assertEqual(
            9,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'hankak\>').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'I \w').count(),
        )

    def test_neexiregex(self):
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2017/0./07/kamakura_golden_week/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_week/*').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_[awe]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_[^abcd]eek/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_(week|monthly)/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2017/05/07/kamakura_golden_we{2}k/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/1{1,2}/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/mount_box_ne\w{2}on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26\Wmount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/2\d/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/\Dount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'i HAVE\shankaku space.').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/\Sount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/11/26/m(o)unt_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'^/Blog/2011/11/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex='/Blog/$').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'Abc\\nDef\\nf').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'Got\\tTab').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'Hello\s+a').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'\<Hankaku').count(),
        )
        self.assertEqual(
            9,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'\<Ankaku').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'Hankaku\>').count(),
        )
        self.assertEqual(
            9,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'Hankak\>').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'i \w').count(),
        )


@unittest.skipUnless(
    ('db_postgresql' in connections and connections['db_postgresql'].vendor == 'postgresql'),
    'only postgresql tests',
)
class RegexLookupPostgreSQLTest(TestCase):
    def setUp(self):
        super(RegexLookupPostgreSQLTest, self).setUp()

        ModelPostgreSQLA.objects.create(id=1, name='/blog/2017/05/07/kamakura_golden_week/')
        ModelPostgreSQLA.objects.create(id=2, name='/blog/2011/11/26/mount_box_net_on_ubuntu/')
        ModelPostgreSQLA.objects.create(id=3, name='I have hankaku space.')
        ModelPostgreSQLA.objects.create(id=4, name=r'abc\ndef\nf')
        ModelPostgreSQLA.objects.create(id=5, name=r'got\ttab')
        ModelPostgreSQLA.objects.create(id=6, name='hello a')
        ModelPostgreSQLA.objects.create(id=7, name='/blog/')
        ModelPostgreSQLA.objects.create(id=8, name='test name')
        ModelPostgreSQLA.objects.create(id=9, name='test name1')

    def tearDown(self):
        super(RegexLookupPostgreSQLTest, self).tearDown()
        ModelPostgreSQLA.objects.all().delete()

    def test_exregex(self):
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exregex=r'/blog/2011/1{1,2}?/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexregex=r'/blog/2011/1{1,2}?/26/mount_box_net_on_ubuntu/').count(),
        )

    def test_iregex(self):
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__exiregex=r'/Blog/2011/1{1,2}?/26/mount_box_net_on_ubuntu/').count(),
        )
        self.assertEqual(
            8,
            ModelPostgreSQLA.objects.filter(name__neexiregex=r'/Blog/2011/1{1,2}?/26/mount_box_net_on_ubuntu/').count(),
        )
