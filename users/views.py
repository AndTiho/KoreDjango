from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')
        return reverse_lazy('catalog:home')