from django.db import models


class ModelPostgreSQLA(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        app_label = 'app_postgresql'


class ModelPostgreSQLB(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        app_label = 'app_postgresql'
