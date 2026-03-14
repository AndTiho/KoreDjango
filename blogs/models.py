from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Заголовок")
    text = models.TextField(null=True, blank=True, verbose_name="Содержимое")
    image = models.ImageField(upload_to="photos/", null=True, blank=True, verbose_name="Изображение")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    viewed_100_times = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.create_at}. Опубликован? = {'Да' if self.published else 'Нет'}"

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = ["views"]
