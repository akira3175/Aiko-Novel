from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class Role(models.Model):
    role_id = models.IntegerField(default=-900)

class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='custom_user')
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

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=40, db_index=True)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


