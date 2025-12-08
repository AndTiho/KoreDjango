from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')

    def __str__(self):
        return f"{self.category_name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = 'категории'
        ordering = ['category_name']

class Product(models.Model):
    product_name = models.CharField(max_length=150, unique=True, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    product_image = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    price = models.FloatField(validators=[MinValueValidator(0.0)], verbose_name="Цена за покупку",default=0.0)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f"{self.product_name} - {self.category}. Цена {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = 'продукты'
        ordering = ['product_name']

class Contacts(models.Model):
    country= models.CharField(max_length=150, verbose_name='Страна')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return f'{self.country} - {self.address}.'

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = "Контакты"