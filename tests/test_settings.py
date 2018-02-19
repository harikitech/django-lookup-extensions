"""Django settings for tests."""
import os


SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'inverse_lookup',
    'tests',
]

if os.environ.get('TEST_DB_VENDOR', None) == 'mysql':
    import pymysql
    pymysql.install_as_MySQLdb()
    DATABASES = {
        'default': {
            'NAME': 'default',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': '',
            'TEST': {
                # https://github.com/hackoregon/devops-17/issues/46#issuecomment-288775868
                'NAME': 'test_' + 'NAME' + os.getenv('TRAVIS_BUILD_NUMBER', "")
            }
        },
    }
elif os.environ.get('TEST_DB_VENDOR', None) == 'postgresql':
    DATABASES = {
        'default': {
            'NAME': 'default',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'TEST': {
                # https://github.com/hackoregon/devops-17/issues/46#issuecomment-288775868
                'NAME': 'test_' + 'NAME' + os.getenv('TRAVIS_BUILD_NUMBER', "")
            }
        },
    }
else:
    DATABASES = {
        'default': {
            'NAME': 'default',
            'ENGINE': 'django.db.backends.sqlite3',
            'TEST': {
                'NAME': 'file:default?mode=memory&cache=shared',
            }
        },
    }
