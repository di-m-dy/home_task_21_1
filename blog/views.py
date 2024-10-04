from django.urls import reverse_lazy, reverse
from pytils.templatetags.pytils_translit import slugify
from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


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
    success_url = reverse_lazy('blog:index')
    form_class = BlogForm

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    success_url = reverse_lazy('blog:index')
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blog:post', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')
