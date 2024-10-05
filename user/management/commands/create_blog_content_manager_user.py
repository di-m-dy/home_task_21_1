from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from blog.models import Blog
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Blog)
        group, created = Group.objects.get_or_create(name='blog_content_manager')
        permission_code_names = (
            'add_blog',
            'change_blog',
            'delete_blog'
        )
        permissions = Permission.objects.filter(codename__in=permission_code_names).all()
        for permission in permissions:
            group.permissions.add(permission)
        user = User.objects.create(
            email='blog_content_manager@example.com',
            first_name='Blog Content Manager',
            last_name='Content Manager Online Store Blog'
        )
        user.groups.add(group)
        user.set_password('12qw34er')
        user.save()
