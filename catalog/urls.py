from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    path('catalog/', views.CategoryView.as_view(), name='catalog'),
    path('category/list/<int:pk>/', views.CategoryListView.as_view(), name='category_list'),

    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/list/', views.ProductListView.as_view(), name='product_list'),
    path('product/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('product/unpublish/<int:pk>/', views.UnPublishProductView.as_view(), name='product_unpublish'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
