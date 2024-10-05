import json
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from user.models import User
from catalog.models import Product, Category
from config.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@example.com',
            first_name='Test User',
            last_name='User Online Store'
        )
        user.set_password('0987')
        user.save()
