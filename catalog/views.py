from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm
from catalog.models import Category, Product, StoreContacts, UserContacts
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView


class IndexListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        data = super().get_queryset()
        return data[:3]


class ContactCreateView(CreateView):
    """
    Отображение статической информаци о контактах с магазином
    Добавление пользовательских данных в базу
    """
    model = UserContacts
    fields = ('first_name', 'last_name', 'email',)

    # добавим в контекст для отображения статических данных
    contact_info = StoreContacts.objects.all()
    extra_context = {
        'contacts': contact_info
    }

    def get_success_url(self):
        new_user_id = self.get_context_data()['object'].id
        return reverse('catalog:thanx', args=[new_user_id])


class ThanxDetailView(DetailView):
    model = UserContacts


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        """
        Переопределение метода запроса
        чтобы динамически фильтровать вывод товара по категориям
        """
        category_id = self.request.GET.get('category_id')
        data = super().get_queryset()
        if category_id:
            data = data.filter(category_id=category_id)

        return data

    def get_context_data(self, **kwargs):
        """
        Переопределение метода
        для добавления в контекст дополнительных объектов
        categories: список объектов категории для фильтрации продуктов
        category: текущая категория
        """
        category_id = self.request.GET.get('category_id')
        data = super().get_context_data()
        categories = Category.objects.all()
        data['categories'] = categories
        data['category'] = get_object_or_404(Category, id=category_id) if category_id else None
        return data


class ProductDetailView(DetailView):
    model = Product


class AddProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm

    def get_success_url(self):
        new_product_id = self.get_context_data()['object'].id
        return reverse('catalog:success_adding_product', args=[new_product_id])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')


class SuccessDeleteTemplateView(TemplateView):
    template_name = 'catalog/success_delete_product.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])


class SuccessAddProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/success_adding_product.html'
