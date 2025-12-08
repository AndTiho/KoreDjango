from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
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


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context={
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context=context )


def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":

        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        product_image = request.FILES.get("product_image")

        #Валидация обязательных полей
        if not all([product_name, description, category_id, price]):
            context = {
                'categories': categories,
                'error': 'Пожалуйста, заполните все обязательные поля.'
            }
            return render(request, "catalog/add_product.html", context)

        # Преобразуем и валидируем цену
        try:
            price = float(price)
            if price <= 0:
                context = {
                    'categories': categories,
                    'error': 'Цена должна быть больше нуля.'
                }
                return render(request, "catalog/add_product.html", context)
        except (ValueError, TypeError):
            context = {
                'categories': categories,
                'error': 'Некорректное значение цены.'
            }
            return render(request, "catalog/add_product.html", context)

        # Получаем объект Category по ID
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            context = {
                'categories': categories,
                'error': 'Выбранная категория не существует.'
            }
            return render(request, "catalog/add_product.html", context)

        # Создаём/обновляем продукт
        try:
            product, created = Product.objects.get_or_create(
                product_name=product_name,
                defaults={
                    'description': description,
                    'category': category,
                    'price': price,
                    'product_image': product_image
                }
            )

            if created:
                print(f'Successfully added product: {product.product_name}')
                return HttpResponse(f'Ваш товар с именем {product_name} успешно создан.')
            else:
                print(f'Product already exists: {product.product_name}')
                context = {
                    'categories': categories,
                    'error': f'Товар {product_name} уже существует.'
                }
                return render(request, "catalog/add_product.html", context)

        except Exception as e:
            context = {
                'categories': categories,
                'error': f'Ошибка при сохранении: {str(e)}'
            }
            return render(request, "catalog/add_product.html", context)

    # Для GET-запроса
    context = {
        'categories': categories
    }
    return render(request, "catalog/add_product.html", context)
