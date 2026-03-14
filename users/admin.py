from django.contrib import admin

from .models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
