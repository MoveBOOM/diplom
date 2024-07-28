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
    get_contacts_view, delete_contact_view, delete_product_view, add_item_to_cart, cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('import-shop-data/', import_shop_data, name='import-shop-data'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('registration/', registration, name='product-list'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_contact/', add_contact_view, name='add_contact'),
    path('contacts/', get_contacts_view, name='get_contacts'),
    path('delete_contact/<int:contact_id>/', delete_contact_view, name='delete_contact'),
    path('cart/delete_product/<int:product_id>/', delete_product_view, name='delete_product'),
    path('cart/', cart, name='cart'),
    path('add_product_to_cart/<int:product_id>/', add_item_to_cart, name='add_product_to_cart'),
]
