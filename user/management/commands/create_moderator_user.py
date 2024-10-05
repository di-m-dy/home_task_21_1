from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from user.models import User
from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)
        group, created = Group.objects.get_or_create(name='moderator')
        permissions = Permission.objects.filter(
            codename__in=("set_published", "edit_description", "change_category_product"),
            content_type=content_type
        )
        user = User.objects.create(
            email='moderator@example.com',
            first_name='Moderator',
            last_name='Moderator Online Store'
        )
        # for permission in permissions:
        #     user.user_permissions.add(permission)
        user.groups.add(group)
        user.set_password('0987')
        user.save()
