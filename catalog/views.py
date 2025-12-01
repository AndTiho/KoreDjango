from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Контролер рендеринга главной страницы"""
    return render(request, 'catalog/home.html')

def contacts(request):
    """Контролер рендеринга страницы контактов"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f'Уважаемый {name}, с номером {phone}. Ваше сообщение << {message} >> получено!')
    return render(request, "catalog/contacts.html")
