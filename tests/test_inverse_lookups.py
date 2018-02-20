import unittest

from django.db import connection, connections
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

from inverse_lookup.lookups import (
    NeContains,
    NeEndsWith,
    NeExact,
    NeIContains,
    NeIEndsWith,
    NeIExact,
    NeIStartsWith,
    NeStartsWith,
    VENDOR_DIALECT,
)
from .models import (
    ModelA,
    ModelB,
    ModelMySQLA,
    ModelMySQLB,
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
        self.compiler = self.query.get_compiler(connection=connection)
        self.field = ModelA._meta.get_field('name')
        self.other_field = ModelB._meta.get_field('name')

        self.sqlite_dialect = VENDOR_DIALECT['sqlite']
        self.mysql_dialect = VENDOR_DIALECT['mysql']
        self.postgresql_dialect = VENDOR_DIALECT['postgresql']

    def tearDown(self):
        super(NeLookupSqliteTest, self).tearDown()

    def test_neexact(self):
        arg = 'test string'

        ne_lookup = NeExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            '"app_default_modela"."name" <> %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])

    def test_neiexact_sqlite(self):
        arg = 'test string'

        lookup = IExact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeIExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])

    def test_necontains_sqlite(self):
        arg = 'test string'

        lookup = Contains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])

    def test_necontains_sqlite_like_with_other_field(self):

        lookup = Contains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neicontains_sqlite(self):
        arg = 'test string'

        lookup = IContains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])

    def test_neicontains_sqlite_like_with_other_field(self):

        lookup = IContains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_nestartswith_sqlite(self):
        arg = 'test string'

        lookup = StartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])

    def test_nestartswith_sqlite_like_with_other_field(self):

        lookup = StartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neistartswith_sqlite(self):
        arg = 'test string'

        lookup = IStartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])

    def test_neistartswith_sqlite_like_with_other_field(self):

        lookup = IStartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%' ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neendswith_sqlite(self):
        arg = 'test string'

        lookup = EndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])

    def test_neendswith_sqlite_like_with_other_field(self):

        lookup = EndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') ESCAPE '\'''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neiendswith_sqlite(self):
        arg = 'test string'

        lookup = IEndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE %s ESCAPE '\'''',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" NOT LIKE %s ESCAPE '\'''',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])

    def test_neiendswith_sqlite_like_with_other_field(self):

        lookup = IEndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connection)
        self.assertEqual(
            r'''"app_default_modela"."name" LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_default_modelb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) ESCAPE '\'''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connection)
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
        self.compiler = self.query.get_compiler(connection=connections['db_mysql'])
        self.field = ModelMySQLA._meta.get_field('name')
        self.other_field = ModelMySQLB._meta.get_field('name')

    def tearDown(self):
        super(NeLookupMySqlTest, self).tearDown()

    def test_neexact(self):
        arg = 'test string'

        lookup = Exact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` = %s',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` <> %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])

    def test_neiexact_mysql(self):
        arg = 'test string'

        lookup = IExact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeIExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])

    def test_necontains_mysql(self):
        arg = 'test string'

        lookup = Contains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE BINARY %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE BINARY %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])

    def test_necontains_mysql_like_with_other_field(self):

        lookup = Contains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neicontains_mysql(self):
        arg = 'test string'

        lookup = IContains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])

    def test_neicontains_mysql_like_with_other_field(self):

        lookup = IContains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_nestartswith_mysql(self):
        arg = 'test string'

        lookup = StartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE BINARY %s',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE BINARY %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])

    def test_nestartswith_mysql_like_with_other_field(self):

        lookup = StartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE BINARY CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE BINARY CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neistartswith_mysql(self):
        arg = 'test string'

        lookup = IStartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])

    def test_neistartswith_mysql_like_with_other_field(self):

        lookup = IStartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE CONCAT(REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'), '%%')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neendswith_mysql(self):
        arg = 'test string'

        lookup = EndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE BINARY %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE BINARY %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])

    def test_neendswith_mysql_like_with_other_field(self):

        lookup = EndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE BINARY CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neiendswith_mysql(self):
        arg = 'test string'

        lookup = IEndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            '`app_mysql_modelmysqla`.`name` NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])

    def test_neiendswith_mysql_like_with_other_field(self):

        lookup = IEndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_mysql'])
        self.assertEqual(
            r'''`app_mysql_modelmysqla`.`name` NOT LIKE CONCAT('%%', REPLACE(REPLACE(REPLACE((`app_mysql_modelmysqlb`.`name`), '\\', '\\\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])


@unittest.skipUnless(
    'db_postgresql' in connections and connections['db_postgresql'].vendor == 'postgresql',
    'postgresql tests',
)
class NeLookupPostgreSQLTest(TestCase):
    def setUp(self):
        super(NeLookupPostgreSQLTest, self).setUp()
        self.query = Query(ModelPostgreSQLA)
        self.compiler = self.query.get_compiler(connection=connections['db_postgresql'])
        self.field = ModelPostgreSQLA._meta.get_field('name')
        self.other_field = ModelPostgreSQLB._meta.get_field('name')

        self.sqlite_dialect = VENDOR_DIALECT['sqlite']
        self.mysql_dialect = VENDOR_DIALECT['mysql']
        self.postgresql_dialect = VENDOR_DIALECT['postgresql']

    def tearDown(self):
        super(NeLookupPostgreSQLTest, self).tearDown()

    def test_neexact(self):
        arg = 'test string'

        lookup = Exact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name" = %s',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name" <> %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])

    def test_neiexact_postgresql(self):
        arg = 'test string'

        lookup = IExact(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) = UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual([arg], lookup_sql[1])

        ne_lookup = NeIExact(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) <> UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg], ne_lookup_sql[1])

    def test_necontains_postgresql(self):
        arg = 'test string'

        lookup = Contains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])

    def test_necontains_postgresql_like_with_other_field(self):

        lookup = Contains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neicontains_postgresql(self):
        arg = 'test string'

        lookup = IContains(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg + '%'], ne_lookup_sql[1])

    def test_neicontains_postgresql_like_with_other_field(self):

        lookup = IContains(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIContains(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_nestartswith_postgresql(self):
        arg = 'test string'

        lookup = StartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])

    def test_nestartswith_postgresql_like_with_other_field(self):

        lookup = StartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text LIKE REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r""""app_postgresql_modelpostgresqla"."name"::text NOT LIKE REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_') || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neistartswith_postgresql(self):
        arg = 'test string'

        lookup = IStartsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual([arg + '%'], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual([arg + '%'], ne_lookup_sql[1])

    def test_neistartswith_postgresql_like_with_other_field(self):

        lookup = IStartsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIStartsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r"""UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')) || '%%'""",  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neendswith_postgresql(self):
        arg = 'test string'

        lookup = EndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text LIKE %s',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            '"app_postgresql_modelpostgresqla"."name"::text NOT LIKE %s',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])

    def test_neendswith_postgresql_like_with_other_field(self):

        lookup = EndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r'''"app_postgresql_modelpostgresqla"."name"::text LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r'''"app_postgresql_modelpostgresqla"."name"::text NOT LIKE '%%' || REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_')''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])

    def test_neiendswith_postgresql(self):
        arg = 'test string'

        lookup = IEndsWith(self.field.cached_col, arg)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE UPPER(%s)',
            lookup_sql[0],
        )
        self.assertEqual(['%' + arg], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, arg)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            'UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE UPPER(%s)',
            ne_lookup_sql[0],
        )
        self.assertEqual(['%' + arg], ne_lookup_sql[1])

    def test_neiendswith_postgresql_like_with_other_field(self):

        lookup = IEndsWith(self.field.cached_col, self.other_field.cached_col)
        lookup_sql = lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r'''UPPER("app_postgresql_modelpostgresqla"."name"::text) LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            lookup_sql[0],
        )
        self.assertEqual([], lookup_sql[1])

        ne_lookup = NeIEndsWith(self.field.cached_col, self.other_field.cached_col)
        ne_lookup_sql = ne_lookup.as_sql(self.compiler, connections['db_postgresql'])
        self.assertEqual(
            r'''UPPER("app_postgresql_modelpostgresqla"."name"::text) NOT LIKE '%%' || UPPER(REPLACE(REPLACE(REPLACE(("app_postgresql_modelpostgresqlb"."name"), '\', '\\'), '%%', '\%%'), '_', '\_'))''',  # noqa E501
            ne_lookup_sql[0],
        )
        self.assertEqual([], ne_lookup_sql[1])
