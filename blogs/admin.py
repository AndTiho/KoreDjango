from django.contrib import admin

from .models import Blog


@admin.register(Blog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "views")
