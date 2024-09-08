from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from pytils.templatetags.pytils_translit import slugify

from blog.models import Blog
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView, UpdateView


# Create your views here.


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        posts = super().get_queryset()
        hidden = self.request.GET.get('hidden')
        if not hidden:
            posts = posts.filter(is_active=True)
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        hidden = self.request.GET.get('hidden')
        if hidden:
            data['hidden'] = True
            print(data)
        return data


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'text', 'image', 'is_active')
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        if form.is_valid():
            print('valid')
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
            print(new_blog.slug)

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'text', 'image', 'is_active')
    success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        return reverse('blog:post', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')
