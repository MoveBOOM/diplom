from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Менеджер для кастомной модели пользователя
class CustomUserManager(BaseUserManager):
    # Метод для создания обычного пользователя
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # Метод для создания суперпользователя
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)

# Кастомная модель пользователя
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

# Модель магазина
class Shop(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")
    url = models.URLField(verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

# Модель категории
class Category(models.Model):
    shops = models.ManyToManyField(Shop, related_name='categories', verbose_name="Магазины")
    name = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# Модель продукта
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


# Модель информации о продукте
class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='info', verbose_name="Продукт")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='info', verbose_name="Магазин")
    name = models.CharField(max_length=128, verbose_name="Название")
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="РРЦ Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Информация о продукте"
        verbose_name_plural = "Информация о продуктах"


# Модель параметра
class Parameter(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

# Модель параметров продукта
class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='parameters',
                                     verbose_name="Информация о продукте")
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name="Параметр")
    value = models.CharField(max_length=128, verbose_name="Значение")

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Параметр продукта"
        verbose_name_plural = "Параметры продуктов"


# Модель заказа
class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Создан'),
        ('DONE', 'Выполнен'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name="Пользователь")
    dt = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    status = models.CharField(choices=STATUS_CHOICES, default="CREATED", max_length=128, verbose_name="Статус")
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name="Контакт", null=True, blank=True)

    def __str__(self):
        return str(self.dt.date()) + " " + self.status + " " + str(self.user)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


# Модель позиции заказа
class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name="Продукт")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"


# Модель контакта
class Contact(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name="Пользователь")
    value = models.JSONField(verbose_name="Контактные данные")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
