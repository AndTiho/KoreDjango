from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "blogs"

urlpatterns = [
    path("blog/home/", views.BlogHome.as_view(), name="blog_home"),
    path("blog/form/", views.BlogCreateView.as_view(), name="blog_form"),
    path("blog/detail/<int:pk>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("blog/list/", views.BlogListView.as_view(), name="blog_list"),
    path("blog/update/<int:pk>/", views.BlogUpdateView.as_view(), name="blog_update"),
    path("blog/delete/<int:pk>/", views.BlogDeleteView.as_view(), name="blog_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
