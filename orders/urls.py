"""
URL configuration for orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from backend.views import import_shop_data, ProductListView, registration, login_view, add_contact_view, \
    get_contacts_view, delete_contact_view, delete_product_view, add_item_to_cart, cart, accept_order_view, done_view

urlpatterns = [
 path('admin/', admin.site.urls),  # Административная панель Django
    path('import-shop-data/', import_shop_data, name='import-shop-data'),  # Импорт данных магазина
    path('products/', ProductListView.as_view(), name='product-list'),  # Список продуктов
    path('registration/', registration, name='product-list'),  # Регистрация пользователя
    path('login/', login_view, name='login'),  # Вход пользователя
    path('logout/', LogoutView.as_view(), name='logout'),  # Выход пользователя
    path('add_contact/', add_contact_view, name='add_contact'),  # Добавление контакта
    path('contacts/', get_contacts_view, name='get_contacts'),  # Получение списка контактов
    path('delete_contact/<int:contact_id>/', delete_contact_view, name='delete_contact'),  # Удаление контакта
    path('cart/delete_product/<int:product_id>/', delete_product_view, name='delete_product'),  # Удаление продукта из корзины
    path('cart/', cart, name='cart'),  # Отображение корзины
    path('add_product_to_cart/<int:product_id>/', add_item_to_cart, name='add_product_to_cart'),  # Добавление продукта в корзину
    path('cart/<int:contact_id>/accept/', accept_order_view, name='accept_order_view'),  # Подтверждение заказа
    path('cart/done/', done_view, name='done_view'),  # Отображение завершенных заказов
]
