from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from utils import send_100views_notification
from .models import Blog

class BlogCreateView(CreateView):
    model = Blog
    fields = ['name', 'text', 'image', 'published']
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:blog_list')


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()

        if obj.views >= 100 and not obj.viewed_100_times:
            send_100views_notification(obj)
            obj.viewed_100_times = True
            obj.save(update_fields=['viewed_100_times'])

        return obj

class BlogHome(ListView):
    model = Blog
    template_name = 'blogs/blog_home.html'
    context_object_name = 'page_obj'
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(published=True).order_by('-views')
        paginator = Paginator(blogs, self.paginate_by)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['name', 'text', 'image', 'published']
    template_name = 'blogs/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blogs:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs:blog_list')

