from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('search', views.search),
    path('register/', views.register, name="register"),
    path('loginPage/', views.loginPage, name="login"),
    path('logoutPage/', views.logoutPage, name="logout"),
]
