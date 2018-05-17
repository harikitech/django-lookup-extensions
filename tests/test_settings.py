"""Django settings for tests."""
import os

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'lookup_extensions',
    'tests',
    'tests.app_default',
    'tests.app_mysql',
    'tests.app_postgresql',
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
            'NAME': 'test_db_mysql_' + os.getenv('TRAVIS_JOB_NUMBER', "").replace('.', '_')
        }
    }

if os.environ.get('TEST_WITH_POSTGRESQL', None) == 'yes':
    if os.environ.get('TEST_USE_CFFI', None) == 'yes':
        from psycopg2cffi import compat
        compat.register()
    DATABASES['db_postgresql'] = {
        'NAME': 'db_postgresql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'TEST': {
            # https://github.com/hackoregon/devops-17/issues/46#issuecomment-288775868
            'NAME': 'test_db_postgresql_' + os.getenv('TRAVIS_JOB_NUMBER', "").replace('.', '_')
        }
    }
elif os.environ.get('TEST_WITH_REDSHIFT', None) == 'yes':
    DATABASES['db_postgresql'] = {
        'NAME': 'testredshift',
        'ENGINE': 'django_redshift_backend',
        'USER': '<REDSHIFT_USER>',
        'PASSWORD': '<REDSHIFT_PASSWORD>',
        'HOST': '<REDSHIFT_HOST>',
        'PORT': '5439',
        'TEST': {
            'NAME': 'testredshift'
        }
    }

DATABASE_ROUTERS = ['tests.test_routers.TestRouter']
