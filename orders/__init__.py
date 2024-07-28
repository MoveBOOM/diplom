# your_project/your_project/__init__.py
from __future__ import absolute_import, unicode_literals

# Это гарантирует, что Celery приложение будет загружено, когда Django стартует
from .celery import app as celery_app

__all__ = ('celery_app',)
