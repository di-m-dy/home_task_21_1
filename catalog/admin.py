from django.contrib import admin
from catalog.models import Category, Product, StoreContacts, UserContacts


# Register your models here.

@admin.register(StoreContacts)
class StoreContactsAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'link'
    ]


@admin.register(UserContacts)
class UserContactsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email'
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description'
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'price',
        'category'
    ]
    list_filter = ['category']
    ordering = ['name']
    search_fields = ['name', 'description']
