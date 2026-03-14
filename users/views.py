import os

from django.contrib.auth.views import LoginView
# from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from dotenv import load_dotenv

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser

load_dotenv(override=True)


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [
            user_email,
        ]
        send_mail(subject, message, from_email, recipient_list)


class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = "users/profile_detail.html"
    context_object_name = "profile"


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm  # Используем новую форму
    template_name = "users/profile_update.html"

    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"pk": self.object.pk})


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("admin:index")
        return reverse_lazy("catalog:home")
