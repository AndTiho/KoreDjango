from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name= 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name="add_product")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)