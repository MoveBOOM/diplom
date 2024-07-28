from django.contrib import admin

from .models import (
    CustomUser, Shop, Category, Product, ProductInfo, Parameter,
    ProductParameter, Order, Orderitem, Contact
)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'shop', 'quantity', 'price', 'price_rrc')
    search_fields = ('name', 'product__name', 'shop__name')


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ('product_info', 'parameter', 'value')
    search_fields = ('product_info__name', 'parameter__name', 'value')


# Настройка отображения модели Order в админке
class OrderAdmin(admin.ModelAdmin):
    list_display = ('dt', 'status', 'user')
    search_fields = ('user__email', 'status')
    list_filter = ('status',)


class OrderitemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'shop', 'quantity')
    search_fields = ('order__id', 'product__name', 'shop__name')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'value')
    search_fields = ('user__email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Orderitem, OrderitemAdmin)
admin.site.register(Contact, ContactAdmin)