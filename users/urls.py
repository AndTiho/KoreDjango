from django.urls import path
from .views import RegisterView, CustomLoginView
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'users'



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('profile/detail/<int:pk>/', views.CustomUserDetailView.as_view(), name='profile_detail'),
    path('profile/update/<int:pk>/', views.CustomUserUpdateView.as_view(), name='profile_update'),

]
