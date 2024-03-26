from django.db import models
from django import forms
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class Role(models.Model):
    role_id = models.IntegerField(default=-900)

class User(models.Model):
    username = models.CharField(max_length=40, db_index=True, primary_key=True, default="nullusername")
    email = models.EmailField(max_length=100, unique=True, default="nullemail@an.com")
    password = models.CharField(max_length=40, default="nullpassword")
    full_name = models.CharField(max_length=100, null=True)
    date_join = models.DateTimeField(default=timezone.now)
    img_avatar = models.URLField(max_length=100, null=True)
    img_background = models.URLField(max_length=100, null=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, default=-900)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class Group(models.Model):
    groupname = models.CharField(max_length=40, db_index=True)
    
    def __str__(self) -> str:
        return self.groupname
    
    
class Member(models.Model):
    auth_user = models.ForeignKey(AuthUser, related_name='members', on_delete=models.CASCADE)  
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    teamrole = models.CharField(max_length=40, db_index=True, default="member")

    def __str__(self):
        return f'{self.auth_user.username}  (gr: {self.group.groupname})'
    
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupname']