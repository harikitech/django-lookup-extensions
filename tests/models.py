from django.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        app_label = 'app_default'


class ModelB(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        app_label = 'app_default'


class ModelMySQLA(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        app_label = 'app_mysql'


class ModelMySQLB(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        app_label = 'app_mysql'


class ModelPostgreSQLA(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        app_label = 'app_postgresql'


class ModelPostgreSQLB(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        app_label = 'app_postgresql'
