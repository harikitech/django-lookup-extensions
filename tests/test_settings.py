"""Django settings for tests."""

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
        },
    },
}
