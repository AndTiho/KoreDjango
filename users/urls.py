from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import CustomLoginView, RegisterView

app_name = "users"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="catalog:home"), name="logout"),
    path("profile/detail/<int:pk>/", views.CustomUserDetailView.as_view(), name="profile_detail"),
    path("profile/update/<int:pk>/", views.CustomUserUpdateView.as_view(), name="profile_update"),
]
