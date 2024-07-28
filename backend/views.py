from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import QuerySet, F
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
import yaml
from django.db import transaction
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, CustomUser, Contact, Order, \
    Orderitem
from .serializer import ProductSerializer, ContactSerializer, OrderItemSerializer, OrderDoneSerializer
from .utils import send_email


@api_view(['POST'])
def import_shop_data(request):
    # Проверяем, есть ли файл в запросе
    if 'file' not in request.FILES:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    file: bytes = request.FILES['file']

    try:
        # Загружаем данные YAML из файла
        data: dict = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        return Response({"error": "Invalid YAML file"}, status=status.HTTP_400_BAD_REQUEST)

    # Извлекаем название магазина, категории и данные о товарах из YAML файла
    shop_name: str = data.get('shop')
    categories_data: list = data.get('categories', [])
    goods_data: list = data.get('goods', [])
    with transaction.atomic():
        # Получаем или создаем экземпляр магазина
        shop, _ = Shop.objects.get_or_create(name=shop_name)

        categories = {}

        # Создаем категории по массиву данных
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(
                id=category_data['id'],
                defaults={'name': category_data['name']}
            )
            categories[category_data['id']] = category
            category.shops.add(shop)

        # Создаем продукты по массиву данных
        for good in goods_data:
            category: Category = categories.get(good['category'])
            if not category:
                continue  # Skip goods with invalid category

            product, _ = Product.objects.get_or_create(
                id=good['id'],
                defaults={
                    'category': category,
                    'name': good['name']
                }
            )

            product_info, _ = ProductInfo.objects.get_or_create(
                product=product,
                shop=shop,
                defaults={
                    'name': good['name'],
                    'quantity': good['quantity'],
                    'price': good['price'],
                    'price_rrc': good['price_rrc']
                }
            )

            # Добавляем параметры продукта
            for key, value in good['parameters'].items():
                parameter, _ = Parameter.objects.get_or_create(name=key)
                ProductParameter.objects.get_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={'value': value}
                )
    return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)


# Представление списка продуктов с фильтрацией и поиском
class ProductListView(generics.ListAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'product__category__name']  # Поля для фильтрации
    search_fields = ['name', 'product__name', 'shop__name']  # Поля для поиска


# Представление для регистрации пользователя
@api_view(['POST'])
def registration(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    # Проверка на заполненность всех полей
    if not first_name or not last_name or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка на существование пользователя с таким email
    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    # Создание нового пользователя
    user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
    # Создание токена для пользователя
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_201_CREATED)


# Представление для входа пользователя
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Проверка на заполненность полей email и password
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Аутентификация пользователя
    user = authenticate(request, username=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Представление для добавления контакта
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_contact_view(request):
    serializer = ContactSerializer(data={'value': request.data})
    if serializer.is_valid():
        Contact.objects.create(user=request.user, value=serializer.data)
        return Response({"message": "Contact added successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление для получения списка контактов
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contacts_view(request):
    contacts = Contact.objects.filter(user=request.user).only('value')
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)


# Представление для удаления контакта
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_contact_view(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    contact.delete()
    return Response({"message": "Contact deleted successfully"}, status=status.HTTP_200_OK)


# Представление для удаления товара из корзины
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_view(request, product_id):
    user = request.user
    order = Order.objects.filter(user=user, status='CREATED').first()

    order_item = get_object_or_404(Orderitem, order=order.id, product_id=product_id)

    if order_item.quantity == 1:
        order_item.delete()
    else:
        order_item.quantity -= 1
        order_item.save(update_fields=['quantity'])

    return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)


# Представление для отображения корзины
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    order = Order.objects.filter(user=user, status='CREATED').first()
    if not order:
        order = Order.objects.create(
            user=user
        )

    # Сериализация элементов заказа с аннотированием полей
    serializer = OrderItemSerializer(
        data=list(order.items.all().annotate(name=F('product__product__name'),
                                             price=F('product__price') * F('quantity')).values()),
        many=True)

    # Проверка валидности данных сериализатора
    if serializer.is_valid():
        result = {"items": serializer.data, "order_id": order.id, "total_price": sum([item['price'] for item in serializer.data])}
        return Response(data=result, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление для добавления товара в корзину
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request, product_id):
    user = request.user
    # Проверка существования заказа со статусом 'CREATED'
    orders: QuerySet = Order.objects.filter(status='CREATED', user_id=user.id)

    if orders.exists():
        order = orders[0]

    else:
        order = Order.objects.create(
            user=user
        )

    # Проверка существования элемента заказа с данным продуктом
    orders_item: QuerySet = Orderitem.objects.filter(order=order.id, product_id=product_id)

    if orders_item.exists():
        order_item: Orderitem = orders_item[0]
        order_item.quantity += 1
        order_item.save(update_fields=['quantity'])

    else:
        product = ProductInfo.objects.get(id=product_id)
        order_item = Orderitem.objects.create(
            order=order,
            quantity=1,
            product_id=product_id,
            shop=product.shop
        )

    return Response({"message": "Order add"}, status=status.HTTP_200_OK)


# Представление для подтверждения заказа
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_order_view(request, contact_id):
    user = request.user

    order = user.order_set.filter(status='CREATED').first()
    contact = Contact.objects.filter(id=contact_id, user=request.user).first()

    if order and contact and order.items.exists():
        order.contact = contact
        order.status = 'DONE'
        order.save(update_fields=['status', 'contact'])
        send_email.delay("Заказ оформлен", "Ваш заказ успешно оформлен", user.email)
        return Response({"message": "OK"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Contact or Order not found"}, status=status.HTTP_400_BAD_REQUEST)


# Представление для отображения завершенных заказов
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def done_view(request):
    user = request.user

    orders = Order.objects.filter(status='DONE', user=user)
    my_serializer = OrderDoneSerializer(orders, many=True)
    return Response(my_serializer.data, status=status.HTTP_200_OK)
