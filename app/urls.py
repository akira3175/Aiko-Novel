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
    path('member-of-trans-team/<int:group_id>', views.memberOfTransTeam, name="member-of-trans-team"),
    path('want-to-join/<int:group_id>', views.wantToJoin, name='want_to_join'),
    path('approve-member/<int:group_id>/<int:member_id>', views.approveMember, name='approve_member'),
    path('change-role-to-admin/<int:group_id>/<int:member_id>', views.changeRoleToAdmin, name='change_role_to_admin'),
    path('change-role-to-owner/<int:group_id>/<int:member_id>', views.changeRoleToOwner, name='change_role_to_owner'),
    path('delete-role-of-admin/<int:group_id>/<int:member_id>', views.deleteRoleOfAdmin, name='delete_role_of_admin'),
    path('delete-group/<int:group_id>', views.deleteGroup, name='delete_group'),
    path('delete-member/<int:group_id>/<int:member_id>', views.deleteMember, name='delete_member'),
    path('out-group/<int:group_id>', views.outGroup, name='out_group'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)