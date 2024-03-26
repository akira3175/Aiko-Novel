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
    path('novel-of-trans-team', views.novelOfTransTeam, name="novel-of-trans-team"),
    path('member-of-trans-team/<int:group_id>', views.memberOfTransTeam, name="member-of-trans-team"),
    path('delete-member/<int:group_id>/<int:member_id>', views.deleteMember, name='delete_member'),
    path('novel-works', views.novelWorks, name="novel-works"),
]
