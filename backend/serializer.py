from rest_framework import serializers

from backend.models import Orderitem, Order, ProductInfo, ProductParameter

# наименование
# описание
# поставщик
# характеристики
# цена
# количество


# Сериализатор для параметров продукта
class ParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source='parameter.name')
    value = serializers.CharField(max_length=128)

    class Meta:
        model = ProductParameter
        fields = ['name', 'value']


# Сериализатор для информации о продукте
class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source='product.name')
    description = serializers.CharField(source='name')
    shop = serializers.CharField(source='shop.name')
    parameters = serializers.ListSerializer(child=ParameterSerializer())

    class Meta:
        model = ProductInfo
        fields = ['id', 'name', 'description', 'shop', 'parameters', 'price', 'quantity']


# Сериализатор для адреса
class AddressSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=128, required=False)
    street = serializers.CharField(max_length=128, required=False)
    house = serializers.CharField(max_length=128, required=False)
    flat = serializers.CharField(max_length=128, required=False)
    build = serializers.CharField(max_length=128, required=False)
    corps = serializers.CharField(max_length=128, required=False)


# Сериализатор для контактной информации
class ContactSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    value = serializers.JSONField()


# Сериализатор для элемента завершенного заказа
class OrderDoneItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.product.name', read_only=True)
    price = serializers.SerializerMethodField() #

    def get_price(self, obj):
        return obj.product.price * obj.quantity

    class Meta:
        model = Orderitem
        fields = ['name', 'quantity', 'price']


# Сериализатор для элемента заказа
class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.product.id')
    name = serializers.CharField(max_length=128)
    price = serializers.FloatField()

    class Meta:
        model = Orderitem
        fields = ['id', 'name', 'price', 'quantity']


# Сериализатор для завершенного заказа
class OrderDoneSerializer(serializers.ModelSerializer):
    items = OrderDoneItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items', 'dt']
