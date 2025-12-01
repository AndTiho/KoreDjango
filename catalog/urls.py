from django.urls import path
from . import views

app_name= 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    # path('submit_data/', views.submit_data, name='submit_data'),
    # path('item/<int:item_id>/', views.show_item, name='show_item')
]