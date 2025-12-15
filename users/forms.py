from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    usable_password = None

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите почту'
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })


        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })


        # self.fields['product_image'].help_text = (
        #     'Поддерживаются форматы: JPEG, JPG, PNG. Максимальный размер: 5 МБ.'
        # )

