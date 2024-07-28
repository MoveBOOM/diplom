from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status, generics
import yaml
from django.db import transaction
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, CustomUser
from .serializer import ProductSerializer


@api_view(['POST'])
def import_shop_data(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    file: bytes = request.FILES['file']

    try:
        data: dict = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        return Response({"error": "Invalid YAML file"}, status=status.HTTP_400_BAD_REQUEST)

    shop_name: str = data.get('shop')
    categories_data: list = data.get('categories', [])
    goods_data: list = data.get('goods', [])
    with transaction.atomic():
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

            # Add product parameters
            for key, value in good['parameters'].items():
                parameter, _ = Parameter.objects.get_or_create(name=key)
                ProductParameter.objects.get_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={'value': value}
                )

    return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)


class ProductListView(generics.ListAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'product__category__name']  # Поля для фильтрации
    search_fields = ['name', 'product__name', 'shop__name']  # Поля для поиска


@api_view(['POST'])
def registration(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not first_name or not last_name or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
    return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)