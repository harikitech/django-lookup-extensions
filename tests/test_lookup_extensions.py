import unittest

from django.db import connection, connections, router
from django.db.models.lookups import (
    Contains,
    EndsWith,
    Exact,
    IContains,
    IEndsWith,
    IExact,
    IStartsWith,
    StartsWith,
)
from django.db.models.sql.query import Query
from django.test import TestCase

from lookup_extensions.lookups import (
    NeContains,
    NeEndsWith,
    NeExact,
    NeIContains,
    NeIEndsWith,
    NeIExact,
    NeIStartsWith,
    NeStartsWith,
)
from tests.app_default.models import (
    ModelA,
    ModelB,
)
from tests.app_mysql.models import (
    ModelMySQLA,
    ModelMySQLB,
)
from tests.app_postgresql.models import (
    ModelPostgreSQLA,
    ModelPostgreSQLB,
)


@unittest.skipUnless(
    connection.vendor == 'sqlite',
    'sqlite tests',
)
class NeLookupSqliteTest(TestCase):
    def setUp(self):
        super(NeLookupSqliteTest, self).setUp()
        self.query = Query(ModelA)
        self.using_connection = connections[router.db_for_read(ModelA)]
        self.compiler = self.query.get_compiler(connection=self.using_connection)
        self.field = ModelA._meta.get_field('name')
        self.other_field = ModelB._meta.get_field('name')

        ModelA.objects.create(name='test name')
        ModelA.objects.create(name='test name1')

    def tearDown(self):
        super(NeLookupSqliteTest, self).tearDown()

    def test_neexact(self):
        arg = 'test string'

        ne_lookup = NeExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_default_modela"."name" <> %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neexact='test name').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__neexact='test Name').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__neexact='test name9').count(),
        )

    def test_neiexact_sqlite(self):
        arg = 'test string'

        lookup = IExact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeIExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neiexact='test name').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neiexact='test Name').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__neiexact='test name9').count(),
        )

    def test_necontains_sqlite(self):
        arg = 'test string'

        lookup = Contains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelA.objects.filter(name__necontains='test name').count(),
        )
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            0,
            ModelA.objects.filter(name__necontains='test Name').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__necontains='test Name1').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__necontains='est nam').count(),
        )

    def test_necontains_sqlite_like_with_other_field(self):

        lookup = Contains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neicontains_sqlite(self):
        arg = 'test string'

        lookup = IContains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelA.objects.filter(name__neicontains='test name').count(),
        )
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            0,
            ModelA.objects.filter(name__neicontains='test Name').count(),
        )
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neicontains='test Name1').count(),
        )
        self.assertEqual(
            0,
            ModelA.objects.filter(name__neicontains='est nam').count(),
        )

    def test_neicontains_sqlite_like_with_other_field(self):

        lookup = IContains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_nestartswith_sqlite(self):
        arg = 'test string'

        lookup = StartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelA.objects.filter(name__nestartswith='test').count(),
        )
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            0,
            ModelA.objects.filter(name__nestartswith='Test').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__nestartswith='est Name').count(),
        )

    def test_nestartswith_sqlite_like_with_other_field(self):

        lookup = StartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neistartswith_sqlite(self):
        arg = 'test string'

        lookup = IStartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelA.objects.filter(name__neistartswith='test').count(),
        )
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            0,
            ModelA.objects.filter(name__neistartswith='Test').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__neistartswith='est Name').count(),
        )

    def test_neistartswith_sqlite_like_with_other_field(self):

        lookup = IStartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neendswith_sqlite(self):
        arg = 'test string'

        lookup = EndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neendswith='name').count(),
        )
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neendswith='Name').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__neendswith='test Nam').count(),
        )

    def test_neendswith_sqlite_like_with_other_field(self):

        lookup = EndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neiendswith_sqlite(self):
        arg = 'test string'

        lookup = IEndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neiendswith='name').count(),
        )
        # https://stackoverflow.com/a/973665
        self.assertEqual(
            1,
            ModelA.objects.filter(name__neiendswith='Name').count(),
        )
        self.assertEqual(
            2,
            ModelA.objects.filter(name__neiendswith='test Nam').count(),
        )

    def test_neiendswith_sqlite_like_with_other_field(self):

        lookup = IEndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])


@unittest.skipUnless(
    'db_mysql' in connections and connections['db_mysql'].vendor == 'mysql',
    'mysql tests',
)
class NeLookupMySqlTest(TestCase):
    def setUp(self):
        super(NeLookupMySqlTest, self).setUp()
        # When running test using MySQL, you may need to change Index size 2048 to 768...
        # analytics/properties/projects/migrations/0003_add_index_to_value.py
        self.query = Query(ModelMySQLA)
        self.using_connection = connections[router.db_for_read(ModelMySQLA)]
        self.compiler = self.query.get_compiler(connection=self.using_connection)
        self.field = ModelMySQLA._meta.get_field('name')
        self.other_field = ModelMySQLB._meta.get_field('name')

        ModelMySQLA.objects.create(name='test name')
        ModelMySQLA.objects.create(name='test name1')

    def tearDown(self):
        super(NeLookupMySqlTest, self).tearDown()
        ModelMySQLA.objects.all().delete()

    def test_neexact(self):
        arg = 'test string'

        lookup = Exact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` = %s',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` <> %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neexact='test name').count(),
        )
        # this is the mysql!
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neexact='test Name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neexact='test name9').count(),
        )

    def test_neiexact_mysql(self):
        arg = 'test string'

        lookup = IExact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeIExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neiexact='test name').count(),
        )
        # this is mysql!
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neiexact='test Name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neiexact='test name9').count(),
        )

    def test_necontains_mysql(self):
        arg = 'test string'

        lookup = Contains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE BINARY %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE BINARY %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__necontains='test name').count(),
        )
        # NOT LIKE BINARY
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__necontains='test Name').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__necontains='test name1').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__necontains='est nam').count(),
        )

    def test_necontains_mysql_like_with_other_field(self):

        lookup = Contains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neicontains_mysql(self):
        arg = 'test string'

        lookup = IContains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__neicontains='test name').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__neicontains='test Name').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neicontains='test name1').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__neicontains='est nam').count(),
        )

    def test_neicontains_mysql_like_with_other_field(self):

        lookup = IContains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_nestartswith_mysql(self):
        arg = 'test string'

        lookup = StartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE BINARY %s',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE BINARY %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__nestartswith='test').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__nestartswith='Test').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__nestartswith='est name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__nestartswith='est Name').count(),
        )

    def test_nestartswith_mysql_like_with_other_field(self):

        lookup = StartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE BINARY CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE BINARY CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neistartswith_mysql(self):
        arg = 'test string'

        lookup = IStartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__neistartswith='test').count(),
        )
        self.assertEqual(
            0,
            ModelMySQLA.objects.filter(name__neistartswith='Test').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neistartswith='est name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neistartswith='est Name').count(),
        )

    def test_neistartswith_mysql_like_with_other_field(self):

        lookup = IStartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neendswith_mysql(self):
        arg = 'test string'

        lookup = EndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE BINARY %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE BINARY %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neendswith='name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neendswith='Name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neendswith='test nam').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neendswith='test Nam').count(),
        )

    def test_neendswith_mysql_like_with_other_field(self):

        lookup = EndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neiendswith_mysql(self):
        arg = 'test string'

        lookup = IEndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neiendswith='name').count(),
        )
        self.assertEqual(
            1,
            ModelMySQLA.objects.filter(name__neiendswith='Name').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neiendswith='test nam').count(),
        )
        self.assertEqual(
            2,
            ModelMySQLA.objects.filter(name__neiendswith='test Nam').count(),
        )

    def test_neiendswith_mysql_like_with_other_field(self):

        lookup = IEndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])


@unittest.skipUnless(
    ('db_postgresql' in connections and connections['db_postgresql'].vendor == 'postgresql' or \
     'db_postgresql' in connections and connections['db_postgresql'].vendor == 'redshift'),
    'postgresql tests',
)
class NeLookupPostgreSQLTest(TestCase):
    def setUp(self):
        super(NeLookupPostgreSQLTest, self).setUp()
        self.query = Query(ModelPostgreSQLA)
        self.using_connection = connections[router.db_for_read(ModelPostgreSQLA)]
        self.compiler = self.query.get_compiler(connection=self.using_connection)
        self.field = ModelPostgreSQLA._meta.get_field('name')
        self.other_field = ModelPostgreSQLB._meta.get_field('name')
        ModelPostgreSQLA.objects.create(id=1, name='test name')
        ModelPostgreSQLA.objects.create(id=2, name='test name1')
    def tearDown(self):
        super(NeLookupPostgreSQLTest, self).tearDown()
        ModelPostgreSQLA.objects.all().delete()

    def test_neexact(self):
        arg = 'test string'

        lookup = Exact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name" = %s',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name" <> %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__neexact='test name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neexact='test Name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neexact='test name9').count(),
        )

    def test_neiexact_postgresql(self):
        arg = 'test string'

        lookup = IExact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) = UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeIExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) <> UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__neiexact='test name').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__neiexact='test Name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neiexact='test name9').count(),
        )

    def test_necontains_postgresql(self):
        arg = 'test string'

        lookup = Contains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__necontains='test name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__necontains='test Name').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__necontains='est nam').count(),
        )

    def test_necontains_postgresql_like_with_other_field(self):

        lookup = Contains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neicontains_postgresql(self):
        arg = 'test string'

        lookup = IContains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__neicontains='test name').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__neicontains='test Name').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__neicontains='est nam').count(),
        )

    def test_neicontains_postgresql_like_with_other_field(self):

        lookup = IContains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_nestartswith_postgresql(self):
        arg = 'test string'

        lookup = StartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__nestartswith='test').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__nestartswith='Test').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__nestartswith='est name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__nestartswith='est Name').count(),
        )

    def test_nestartswith_postgresql_like_with_other_field(self):

        lookup = StartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text LIKE REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text NOT LIKE REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neistartswith_postgresql(self):
        arg = 'test string'

        lookup = IStartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__neistartswith='test').count(),
        )
        self.assertEqual(
            0,
            ModelPostgreSQLA.objects.filter(name__neistartswith='Test').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neistartswith='est name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neistartswith='est Name').count(),
        )

    def test_neistartswith_postgresql_like_with_other_field(self):

        lookup = IStartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neendswith_postgresql(self):
        arg = 'test string'

        lookup = EndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__neendswith='name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neendswith='Name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neendswith='test nam').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neendswith='test Nam').count(),
        )

    def test_neendswith_postgresql_like_with_other_field(self):

        lookup = EndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_postgresql_modelpostgresqla"."name"::text LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''"app_postgresql_modelpostgresqla"."name"::text NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neiendswith_postgresql(self):
        arg = 'test string'

        lookup = IEndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__neiendswith='name').count(),
        )
        self.assertEqual(
            1,
            ModelPostgreSQLA.objects.filter(name__neiendswith='Name').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neiendswith='test nam').count(),
        )
        self.assertEqual(
            2,
            ModelPostgreSQLA.objects.filter(name__neiendswith='test Nam').count(),
        )

    def test_neiendswith_postgresql_like_with_other_field(self):

        lookup = IEndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, self.using_connection)
        self.assertEqual(
            r'''UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])
