from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, StoreContacts, UserContacts, Version
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView


class IndexListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        data = super().get_queryset().order_by('-created_at')
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
        data = super().get_queryset().order_by('-created_at')
        if category_id:
            data = data.filter(category_id=category_id).order_by('-created_at')
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
        data['object_list'] = [{'product': item, 'version': item.version_set.filter(is_current=True).first()} for item in data['object_list']]
        categories = Category.objects.all()
        data['categories'] = categories
        data['category'] = get_object_or_404(Category, id=category_id) if category_id else None
        return data


class ProductDetailView(DetailView):
    model = Product


class AddProductCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('user:login')
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm

    def get_success_url(self):
        new_product_id = self.get_context_data()['object'].id
        return reverse('catalog:success_adding_product', args=[new_product_id])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            data['formset'] = VersionFormset(self.request.POST)
        else:
            data['formset'] = VersionFormset()
        return data

    def form_valid(self, form):
        """
        Валидация
        Проверка на несколько текущих версий
        """
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            instances = formset.save(commit=False)
            check_update = [instance for instance in instances]
            for item in formset.queryset:
                if item not in check_update:
                    check_update.append(item)
            check_current = [item for item in check_update if item.is_current]
            if len(check_current) > 1:
                form.add_error(None, "Может быть только одна версия!")
                return self.form_invalid(form)
            else:
                form.instance.user = self.request.user
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return super().form_valid(form)
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('user:login')
    model = Product
    success_url = reverse_lazy('catalog:products')


class SuccessDeleteTemplateView(TemplateView):
    template_name = 'catalog/success_delete_product.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('user:login')
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            data['formset'] = VersionFormset(instance=self.object)
        return data

    def form_valid(self, form):
        """
        Валидация
        Проверка на несколько текущих версий
        """
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            instances = formset.save(commit=False)
            check_update = [instance for instance in instances]
            for item in formset.queryset:
                if item not in check_update:
                    check_update.append(item)
            check_current = [item for item in check_update if item.is_current]
            if len(check_current) > 1:
                form.add_error(None, "Может быть только одна версия!")
                return self.form_invalid(form)
            else:
                formset.instance = self.object
                formset.save()
                return super().form_valid(form)
        return super().form_invalid(form)


class SuccessAddProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/success_adding_product.html'
