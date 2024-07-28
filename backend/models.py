from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField(verbose_name='URL')
