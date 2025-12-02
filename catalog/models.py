from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')

    def __str__(self):
        return f"{self.category_name} - {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = 'категории'
        ordering = ['category_name']

class Product(models.Model):
    product_name = models.CharField(max_length=150, unique=True, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    product_image = models.ImageField(upload_to='photos/', verbose_name='Изображение')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    price = models.FloatField(verbose_name="Цена за покупку")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f"{self.product_name} - {self.description}. Цена {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = 'продукты'
        ordering = ['product_name']