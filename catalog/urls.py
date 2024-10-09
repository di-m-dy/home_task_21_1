from django.urls import path
from catalog.views import (
    IndexListView,
    ContactCreateView,
    ThanxDetailView,
    ProductDetailView,
    ProductListView,
    AddProductCreateView,
    SuccessAddProductDetailView,
    ProductDeleteView,
    ProductUpdateView,
    SuccessDeleteTemplateView
)
from catalog.services import set_cache_controller

app_name = 'catalog'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('contacts/', ContactCreateView.as_view(), name='contacts'),
    path('product/<int:pk>/', set_cache_controller(ProductDetailView.as_view()), name="product"),
    path('products/', ProductListView.as_view(), name="products"),
    path('add_product/', AddProductCreateView.as_view(), name="add_product"),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='update_product'),
    path('success_delete_product/<int:pk>/', SuccessDeleteTemplateView.as_view(), name='success_delete_product'),
    path('success_adding_product/<int:pk>/', SuccessAddProductDetailView.as_view(), name="success_adding_product"),
    path('thanx/<int:pk>/', ThanxDetailView.as_view(), name='thanx')
]
