from django.db import models


class ModelMySQLA(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        app_label = 'app_mysql'


class ModelMySQLB(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        app_label = 'app_mysql'
