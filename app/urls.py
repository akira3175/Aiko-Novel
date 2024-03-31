from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search),
    path('register', views.register, name="register"),
    path('loginPage', views.loginPage, name="login"),
    path('logoutPage', views.logoutPage, name="logout"),
    path('trans-team', views.transTeam, name="transteam"),
    path('novel-of-trans-team', views.novelOfTransTeam, name="novel-of-trans-team"),
    path('novel-works', views.novelWorks, name="novel-works"),
    path('saveBook', views.saveBook, name='saveBook'),
    path('novel', views.novel, name='novel')
]
 