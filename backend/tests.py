from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import os

from backend.models import Shop, Category, Product


class TestImportShopData(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('import-shop-data')

    def test_import_shop_data(self):
        # Создаем временный YAML файл с тестовыми данными
        test_yaml_data = """
        shop: Связной
        categories:
          - id: 224
            name: Смартфоны
          - id: 15
            name: Аксессуары
        goods:
          - id: 4216292
            category: 224
            model: apple/iphone/xs-max
            name: Смартфон Apple iPhone XS Max 512GB (золотистый)
            price: 110000
            price_rrc: 116990
            quantity: 14
            parameters:
              Диагональ (дюйм): 6.5
              Разрешение (пикс): 2688x1242
              Встроенная память (Гб): 512
              Цвет: золотистый
        """
        temp_yaml_file = 'test_shop.yaml'
        with open(temp_yaml_file, 'w') as file:
            file.write(test_yaml_data)

        # Читаем файл и отправляем его в POST-запросе
        with open(temp_yaml_file, 'rb') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')

        # Проверяем успешное выполнение запроса
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Data imported successfully")

        # Проверяем, что объекты созданы в базе данных
        self.assertTrue(Shop.objects.filter(name="Связной").exists())
        self.assertTrue(Category.objects.filter(id=224, name="Смартфоны").exists())
        self.assertTrue(
            Product.objects.filter(id=4216292, name="Смартфон Apple iPhone XS Max 512GB (золотистый)").exists())

        # Удаляем временный файл
        os.remove(temp_yaml_file)
