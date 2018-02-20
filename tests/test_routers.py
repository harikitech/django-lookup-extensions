

class TestRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'app_default':
            return 'default'
        elif model._meta.app_label == 'app_mysql':
            return 'db_mysql'
        elif model._meta.app_label == 'app_postgresql':
            return 'db_postgresql'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'app_default':
            return 'default'
        elif model._meta.app_label == 'app_mysql':
            return 'db_mysql'
        elif model._meta.app_label == 'app_postgresql':
            return 'db_postgresql'
        return None
