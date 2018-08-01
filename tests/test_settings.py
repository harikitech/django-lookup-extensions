import environ

# Replace backends
environ.Env.DB_SCHEMES['postgres'] = 'lookup_extensions.backends.postgresql'
environ.Env.DB_SCHEMES['mysql'] = 'lookup_extensions.backends.mysql'
environ.Env.DB_SCHEMES['sqlite'] = 'lookup_extensions.backends.sqlite3'
env = environ.Env()


SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'lookup',
    'or_lookups',
    'reverse_lookup',
    'string_lookup',
]
DATABASES = {
    'default': env.db(default='sqlite://:memory:'),
}
if 'lookup_extensions.backends.mysql' == DATABASES['default']['ENGINE']:
    """Create database with specific options for MySQL.
    https://docs.djangoproject.com/en/dev/topics/testing/overview/#the-test-database
    https://docs.djangoproject.com/en/dev/ref/databases/#creating-your-database
    """
    DATABASES['default']['TEST'] = {
        'CHARSET': 'utf8mb4',
        'COLLATION': 'utf8mb4_unicode_ci',
    }
