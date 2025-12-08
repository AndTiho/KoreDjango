from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from .models import Contacts, Product, Category


def home(request):
    """Контроллер рендеринга главной страницы"""

    # latest_products = Product.objects.order_by('-create_at')[:5] - из задания 5 последних добавленных товаров
    products =  Product.objects.all().order_by('-id')

    paginator = Paginator(products, 4)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    """Контролер рендеринга страницы контактов"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f'Уважаемый {name}, с номером {phone}. Ваше сообщение << {message} >> получено!')
    else:  # GET-запрос (или любой другой метод)
        # Получаем все контактные данные из базы
        contacts_data = Contacts.objects.all()

        # Передаем данные в шаблон
        return render(request, "catalog/contacts.html", {
            'contacts': contacts_data
        })

class ProductCreateView(CreateView):
    model = Product
    fields = ['product_name', 'description', 'category', 'price', 'product_image']
    template_name = 'catalog/product_add.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['product_name', 'description', 'category', 'price', 'product_image']
    template_name = 'catalog/product_add.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
