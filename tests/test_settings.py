"""Django settings for tests."""
import os


SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'inverse_lookup',
    'tests',
]

DATABASES = {
    'default': {
        'NAME': 'default',
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'NAME': 'file:default?mode=memory&cache=shared',
        }
    },
    'db_mysql': {
        'NAME': 'db_mysql',
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'NAME': 'file:db_mysql?mode=memory&cache=shared',
        }
    },
    'db_postgresql': {
        'NAME': 'db_postgresql',
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'NAME': 'file:db_postgresql?mode=memory&cache=shared',
        }
    },
}

if os.environ.get('TEST_WITH_OLD_SQLITE', None) == 'yes':
    DATABASES['default'] = {
        'NAME': 'default',
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'NAME': ':memory:',
        }
    }

if os.environ.get('TEST_WITH_MYSQL', None) == 'yes':
    import pymysql
    pymysql.install_as_MySQLdb()
    DATABASES['db_mysql'] = {
        'NAME': 'db_mysql',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '',
        'TEST': {
            # https://github.com/hackoregon/devops-17/issues/46#issuecomment-288775868
            'NAME': 'test_db_mysql' + 'NAME' + os.getenv('TRAVIS_BUILD_NUMBER', "")
        }
    }

if os.environ.get('TEST_WITH_POSTGRES', None) == 'yes':
    if os.environ.get('TEST_USE_CFFI', None) == 'yes':
        from psycopg2cffi import compat
        compat.register()
    DATABASES['db_postgresql'] = {
        'NAME': 'db_postgresql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'TEST': {
            # https://github.com/hackoregon/devops-17/issues/46#issuecomment-288775868
            'NAME': 'test_db_postgresql' + 'NAME' + os.getenv('TRAVIS_BUILD_NUMBER', "")
        }
    }

DATABASE_ROUTERS = ['tests.test_routers.TestRouter']
