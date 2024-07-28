from rest_framework import serializers

from backend.models import Product
#
# наименование
# описание
# поставщик
# характеристики
# цена
# количество


from rest_framework import serializers
from backend.models import Product, ProductInfo, ProductParameter, Shop


class ParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source='parameter.name')
    value = serializers.CharField(max_length=128)

    class Meta:
        model = ProductParameter
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source='product.name')
    description = serializers.CharField(source='name')
    shop = serializers.CharField(source='shop.name')
    parameters = serializers.ListSerializer(child=ParameterSerializer())

    class Meta:
        model = ProductInfo
        fields = ['name', 'description', 'shop', 'parameters', 'price', 'quantity']
