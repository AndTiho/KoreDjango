
from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;")

        category, _ = Category.objects.get_or_create(category_name='Приставки', description='Различные виды игровых устройств')

        products = [
            {'product_name': 'PlayStation 5', 'description': 'Игровая приставка от Японии', 'category':category,
             'price':999, 'product_image': 'photos/PS5.jpg'},
            {'product_name': 'XBox', 'description': 'Игровая приставка от Америки', 'category': category,
             'price': 799}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.product_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.product_name}'))

        call_command('loaddata', 'catalog_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))