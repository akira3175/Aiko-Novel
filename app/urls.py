from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search),
    path('register', views.register, name="register"),
    path('loginPage', views.loginPage, name="login"),
    path('logoutPage', views.logoutPage, name="logout"),
    path('addGroupPane', views.addGroup, name="addgroup"),
    path('trans-team', views.transTeam, name="transteam"),
    path('trans-team', views.list),
    path('novel-of-trans-team', views.novelOfTransTeam, name="novel-of-trans-team"),
    path('member-of-trans-team', views.memberOfTransTeam, name="member-of-trans-team"),
    path('novel-works', views.novelWorks, name="novel-works"),
]
