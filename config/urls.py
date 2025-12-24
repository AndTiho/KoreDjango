from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('catalog/', include('catalog.urls', namespace='catalog')),
                  path('blogs/', include('blogs.urls', namespace='blogs')),
                  path('users/', include('users.urls', namespace='users')),
                  path('accounts/', include('users.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
