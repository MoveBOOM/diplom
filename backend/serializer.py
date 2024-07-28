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


class AddressSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=128, required=False)
    street = serializers.CharField(max_length=128, required=False)
    house = serializers.CharField(max_length=128, required=False)
    flat = serializers.CharField(max_length=128, required=False)
    build = serializers.CharField(max_length=128, required=False)
    corps = serializers.CharField(max_length=128, required=False)


class ContactSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=128)
    middle_name = serializers.CharField(max_length=128)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=128)
    address = AddressSerializer()
