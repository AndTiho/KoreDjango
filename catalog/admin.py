from django.contrib import admin

from .models import Category, Contacts, CustomerData, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")
    search_fields = ("category_name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price", "category", "product_image")
    list_filter = ("category",)
    search_fields = ("product_name", "description")


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("country", "inn", "address")
    search_fields = ("country",)


@admin.register(CustomerData)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "message")
