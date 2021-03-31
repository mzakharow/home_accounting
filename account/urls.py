from django.urls import path
from django.contrib.auth import views as auth_views
from account import views

app_name = "account"

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/', views.edit, name='edit'),
]