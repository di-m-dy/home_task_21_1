# Generated by Django 4.2 on 2024-10-04 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_product_options_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_published', 'Can publish product')], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
    ]
