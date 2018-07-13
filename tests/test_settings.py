import environ


env = environ.Env()


SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'lookup_extensions',
    'lookup',
    'or_lookups',
    'reverse_lookup',
    'string_lookup',
]
DATABASES = {
    'default': env.db(default='sqlite://:memory:'),
}
