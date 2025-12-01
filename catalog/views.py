from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f'Уважаемый {name}, с номером {phone}. Ваше сообщение << {message} >> получено!')
    return render(request, "catalog/contacts.html")




# def show_data(request):
#     if request.method == 'GET':
#         return render(request, 'app/data.html')
#
#
# def submit_data(request):
#     if request.method == 'POST':
#         # Обработка данных формы
#         return HttpResponse("Данные отправлены!")
#
#
# def show_item(request, item_id):
#     return render(request, 'app/item.html', {'item_id':item_id})