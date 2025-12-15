import os

from PIL import Image
from django import forms
from django.core.exceptions import ValidationError

from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'text', 'image', 'published']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите заголовок ( не более 150 символов )'
        })

        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите содержание блога'
        })


        self.fields['published'].widget.attrs.update({
            'class': 'form - check'
        })

        self.fields['image'].help_text = (
            'Поддерживаются форматы: JPEG, JPG, PNG. Максимальный размер: 5 МБ.'
        )

        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file btn-primary',
            'id': 'id_product_image',
        })

    def clean_image(self):
        """ Проверка изображения на соответствие требований:
        1. Верный формат 'jpeg', 'jpg', 'png'
        2. Верный размер < 5 Mb
        3. Доп проверка на случай подмены расширения
        4. Доп проверка на случай если файл не изображение (через Pillow)
        """
        image = self.cleaned_data.get('image')

        if not image:
            return image  # поле необязательно

        # Проверка размера (5 МБ = 5 * 1024 * 1024 байт)
        max_size = 5 * 1024 * 1024  # 5 МБ
        if image.size > max_size:
            raise ValidationError(
                f'Размер файла не должен превышать 5 МБ. Текущий размер: {image.size / 1024 / 1024:.2f} МБ.')

        # Дополнительная проверка расширения (на случай подмены MIME)
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise ValidationError('Недопустимое расширение файла. Используйте .jpg или .png.')

        # Проверка целостности через Pillow
        try:
            img = Image.open(image)
            img.verify()
            img.close()
        except Exception:
            raise ValidationError('Файл повреждён или не является изображением.')

        return image

