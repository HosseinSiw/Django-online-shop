import random
from faker import Faker
from django.core.management import BaseCommand

from ...models import Coupon


class Command(BaseCommand):
    help = "This command creates some random coupons and then inject them into Database."
    sampler = Faker()

    def handle(self, *args, **kwargs):
        for _ in range(10):
            code = self.sampler.country()  # I use random country names, you can change it on your owns.
            percent = random.randint(10, 40)
            Coupon.objects.create(code=code, percent=percent)

        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 records into coupons table.'))
