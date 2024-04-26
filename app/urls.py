from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search),
    path('register', views.register, name="register"),
    path('check-username/', views.checkUsername, name='checkUsername'),
    path('check-email/', views.checkEmail, name='checkEmail'),
    path('login', views.loginPage, name="login"),
    path('logoutPage', views.logoutPage, name="logout"),
    path('addGroupPane', views.addGroup, name="addgroup"),
    path('changePasswordPane', views.changePassword, name='changepassword'), 
    path('changeDescriptionPane/<int:group_id>/', views.changeDescription, name='changedescription'),
    path('trans-team', views.transTeam, name="transteam"),
    path('novel-of-trans-team/<int:group_id>/', views.novelOfTransTeam, name="novel-of-trans-team"),
    path('novel-works/<int:group_id>/<int:book_id>/', views.novelWorks, name="novel-works"),
    path('write/<int:volume_id>/<int:chapter_id>/', views.write, name="write"),
    path('saveBook', views.saveBook, name='saveBook'),
    path('saveBookSub', views.saveBookSub, name='saveBookSub'),
    path('delete-book/<int:book_id>', views.deleteBook, name='delete-book'),
    path('save-volume/', views.saveVolume, name='save-volume'),
    path('delete-volume/<int:volume_id>', views.deleteVolume, name='delete-volume'),
    path('save-chapter/', views.saveChapter, name='save-chapter'),
    path('upload-chapter/', views.uploadChapter, name='upload-chapter'),
    path('delete-chapter/', views.deleteChapter, name='delete-chapter'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('save-background/', views.saveBackground, name='save-background'), 
    path('save-avatar/', views.saveAvatar, name='save-avatar'), 
    path('save-fullname/', views.saveFullName, name="save-fullname"),
    path('group/<int:group_id>', views.group, name='group'),
    path('member-of-trans-team/<int:group_id>', views.memberOfTransTeam, name="member-of-trans-team"),
    path('want-to-join/<int:group_id>', views.wantToJoin, name='want_to_join'),
    path('approve-member/<int:group_id>/<int:member_id>', views.approveMember, name='approve_member'),
    path('change-role-to-admin/<int:group_id>/<int:member_id>', views.changeRoleToAdmin, name='change_role_to_admin'),
    path('change-role-to-owner/<int:group_id>/<int:member_id>', views.changeRoleToOwner, name='change_role_to_owner'),
    path('delete-role-of-admin/<int:group_id>/<int:member_id>', views.deleteRoleOfAdmin, name='delete_role_of_admin'),
    path('delete-group/<int:group_id>', views.deleteGroup, name='delete_group'),
    path('delete-member/<int:group_id>/<int:member_id>', views.deleteMember, name='delete_member'),
    path('out-group/<int:group_id>', views.outGroup, name='out_group'),
    path('novel/<int:id>/', views.novel, name='novel'),
    path('read/<int:chapter_id>/', views.read, name='read'),
    path('library', views.library, name='library'),
    path('follow-book/<int:book_id>', views.followBook, name='followBook'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/ckeditor/', views.ckeditor_admin, name='ckeditor_admin'),
    path('novel/<int:id>/', views.novel, name='novel'),
    path('read/<int:volume_id>/<int:chapter_id>/', views.read, name='read'),
    path('the-loai/<str:category>/', views.category, name='category'),
    path('list/<str:type>/', views.list, name='list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app.views.handler404'