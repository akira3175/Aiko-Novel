from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search),
    path('register', views.register, name="register"),
    path('check-username/', views.checkUsername, name='checkUsername'),
    path('check-email/', views.checkEmail, name='checkEmail'),
    path('loginPage', views.loginPage, name="login"),
    path('logoutPage', views.logoutPage, name="logout"),
    path('addGroupPane', views.addGroup, name="addgroup"),
    path('trans-team', views.transTeam, name="transteam"),
    path('novel-of-trans-team', views.novelOfTransTeam, name="novel-of-trans-team"),
    path('novel-works', views.novelWorks, name="novel-works"),
    path('saveBook', views.saveBook, name='saveBook'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('save-background/', views.saveBackground, name='save-background'), 
    path('save-avatar/', views.saveAvatar, name='save-avatar'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)