from django.core.cache import cache

from config.settings import CACHED_ENABLED
from django.views.decorators.cache import cache_page
from catalog.models import Category

def set_cache_controller(controller):
    """
    Кэширование контроллера
    :param controller: контроллер Controller.as_view()
    """
    if CACHED_ENABLED:
        return cache_page(200)(controller)
    return controller

def get_categories():
    """
    Кэширование выборки категорий
    """
    if CACHED_ENABLED:
        key = f'categories'
        categories = cache.get(key)
        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)
    else:
        categories = Category.objects.all()
    return categories