from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    # path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('add_product/', views.add_product, name="add_product")
    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/list/', views.ProductListView.as_view(), name='product_list'),
    path('product/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
