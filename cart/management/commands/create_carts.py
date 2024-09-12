from django.core.management import BaseCommand
from cart.models import Cart
from users.models import CustomUser as User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            _, created = Cart.objects.get_or_create(user=user)
            print("created:", created)
