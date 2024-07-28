import django
from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField(verbose_name='URL')


class Category(models.Model):
    shops = models.ManyToManyField(Shop, related_name='categories')
    name = models.CharField(max_length=128)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=128)
