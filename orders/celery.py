# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders.settings')

# Создаем экземпляр приложения Celery
app = Celery('orders')

# Загружаем настройки из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим и загружаем задачи из приложений Django
app.autodiscover_tasks()
