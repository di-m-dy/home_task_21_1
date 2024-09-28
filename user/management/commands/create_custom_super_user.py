from django.core.management import BaseCommand
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@example.com',
            first_name='Admin',
            last_name='Online Store',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('1234')
        user.save()
