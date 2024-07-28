from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import yaml
from django.db import transaction
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


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
