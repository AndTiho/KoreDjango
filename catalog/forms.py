import os

from PIL import Image
from django import forms
from django.core.exceptions import ValidationError

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'category', 'price', 'product_image']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите наименование продукта'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание продукта'
        })

        self.fields['category'].help_text = (
            'Выберите категорию из выпадающего списка'
        )


        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'id': 'id_category'
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['product_image'].help_text = (
            'Поддерживаются форматы: JPEG, JPG, PNG. Максимальный размер: 5 МБ.'
        )

        self.fields['product_image'].widget.attrs.update({
            'class': 'form-control-file',
            'id': 'id_product_image',
        })

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Цена не может быть меньше или равна нулю.')
        return price

    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    def clean_product_name(self):
        name = self.cleaned_data.get('product_name')
        if name:
            self._check_forbidden_words(name, 'наименование')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            self._check_forbidden_words(description, 'описание')
        return description

    def _check_forbidden_words(self, text, field_name):
        """Проверка текста на наличие запрещённых слов"""
        text_lower = text.lower()
        for word in self.FORBIDDEN_WORDS:
            if word in text_lower:
                raise ValidationError(
                    f'В {field_name} нельзя использовать слово "{word}".'
                )

    def clean_product_image(self):
        """ Проверка изображения на соответствие требований:
        1. Верный формат 'jpeg', 'jpg', 'png'
        2. Верный размер < 5 Mb
        3. Доп проверка на случай подмены расширения
        4. Доп проверка на случай если файл не изображение (через Pillow)
        """
        image = self.cleaned_data.get('product_image')

        if not image:
            return image  # поле необязательно

        # Проверка формата файла
        file_type = image.content_type.split('/')[1].lower()
        if file_type not in ['jpeg', 'jpg', 'png']:
            raise ValidationError('Допустимы только форматы JPEG и PNG.')

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
