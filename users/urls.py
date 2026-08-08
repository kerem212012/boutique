from django.contrib.auth import views as auth_views
from django.urls import path

from .views import profile_view, register_view

app_name = 'users'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
