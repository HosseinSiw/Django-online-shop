from django.core.management import BaseCommand, CommandError
from ...models import Product, Category
from users.models import CustomUser
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Adds some random products.'
    email = "email@email.com"
    password = "test/123456"
    username = "TEST_USERNAME"

    def add_arguments(self, parser):
        parser.add_argument("num_product", nargs=1, type=int)

    def handle(self, *args, **options):
        sampler = Faker()
        try:
            count = options["num_product"][0]
        except:
            raise CommandError("Number of instances not provided.")
        categories = []
        for _ in range(count):
            name = sampler.name()
            Category.objects.create(name=name)
            categories.append(name)
        try:
            owner = CustomUser.objects.get(email=self.email,)
        except CustomUser.DoesNotExist:
            owner = CustomUser.objects.create_user(email=self.email, password=self.password, username=self.username)

        print(f'Adding {count} products to db...')
        for _ in range(count):
            name = sampler.name()
            price = round(random.uniform(1.0, 100.0), 2)
            size = random.randint(37, 46)
            stock = random.randint(1, 10)
            cat_name = random.choice(categories)
            category = Category.objects.get(name=cat_name)
            Product.objects.create(owner=owner, name=name, price=price, size=size, stock=stock, category=category)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} instances'))
