from django.core.management.base import BaseCommand
from django.db import connection
from config.settings import BASE_DIR
from catalog.models import Category, Product, StoreContacts
import json


class Command(BaseCommand):
    help = "Clear all tables & add default data"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE catalog_storecontacts RESTART IDENTITY CASCADE;')
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;')

        with open(BASE_DIR / 'default_data/data.json') as file:
            data = json.load(file)

        store_contacts = [StoreContacts(id=item['pk'], **item['fields'])
                          for item in data if item['model'] == 'catalog.storecontacts']
        categories = [Category(id=item['pk'], **item['fields'])
                      for item in data if item['model'] == 'catalog.category']
        products = [item for item in data if item['model'] == 'catalog.product']

        StoreContacts.objects.bulk_create(store_contacts)
        Category.objects.bulk_create(categories)

        products_to_db = []
        for item in products:
            item['fields']['category'] = Category.objects.get(id=item['fields']['category'])
            prod = Product(id=item['pk'], **item['fields'])
            products_to_db.append(prod)
        Product.objects.bulk_create(products_to_db)
        print('Success! Add default data')
