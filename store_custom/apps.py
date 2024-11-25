from django.apps import AppConfig
from django.dispatch import receiver
from .signals import order_created
from store.signals.handlers import on_order_created

class StoreCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_custom'

    def ready(self):
        @receiver(order_created)
        def on_order_created(sender, **kwargs):
            print(kwargs['order'])