from django.shortcuts import render
from django.http import HttpResponse
from .models import Contacts, Product


def home(request):
    """Контроллер рендеринга главной страницы"""

    # latest_products = Product.objects.order_by('-create_at')[:5] - из задания 5 последних добавленных товаров
    products = Product.objects.all()

    for product in products:
        print(f"Продукт: {product.product_name}, Цена: {product.price}, Дата: {product.create_at}")

    context = {
        'products': products
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


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context={
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context=context )