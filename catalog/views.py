from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, View

from .models import Contacts, Product, Category, CustomerData
from catalog.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from .services import ProductService


class HomeView(ListView):
    """Класс для рендеринга главной страницы по 4 товара на страницу"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        """Метод для пагинации страниц с товарами"""
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)

class ContactsView(View):
    """Контролер для обработки страницы контактов"""
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        """ Метод для заполнения контактов компании из админки"""
        contacts_data = Contacts.objects.all()
        return render(request, self.template_name, {
            'contacts': contacts_data,
            'form_submitted': False  # для индикации отправки
        })

    def post(self, request, *args, **kwargs):
        """ Метод для записи контактов пользователей в БД"""
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        CustomerData.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        contacts_data = Contacts.objects.all()
        return render(request, self.template_name, {
            'contacts': contacts_data,
            'form_submitted': True,
            'submitted_name': name
        })

class UnPublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет прав на отмену публикации продукта')

        product.published = False
        product.save()

        return redirect('catalog:product_detail', pk= pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс для добавления продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_add.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс для детальной информации по продукту"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductListView(ListView):
    """Класс для просмотра списка всех продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = cache.get('product_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('product_queryset', queryset, 60 * 15)
        return queryset



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """ Класс для изменения информации в продукте"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_add.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        raise PermissionDenied



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if (request.user == self.object.owner
                or request.user.has_perm('catalog.delete_product')):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied


class CategoryView(ListView):
    """Класс для просмотра списка категорий"""
    model = Category
    template_name = 'catalog/catalog.html'
    context_object_name = 'category'


class CategoryListView(ListView):
    """Класс для просмотра списка всех продуктов в заданной категории"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        queryset = cache.get('category_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('category_queryset', queryset, 60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs['pk']

        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['products_be_category'] = ProductService.get_product_list_by_category(category_id)
        return context
