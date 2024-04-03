from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


# Create your models here.
# Change forms register django

"""User model"""

class Role(models.Model):
    role_id = models.IntegerField(default=-900)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
class User(models.Model):
    username = models.CharField(max_length=40, db_index=True, primary_key=True, default="nullusername")
    email = models.EmailField(max_length=100, unique=True, default="nullemail@an.com")
    password = models.CharField(max_length=40, default="nullpassword")
    full_name = models.CharField(max_length=100, null=True)
    date_join = models.DateTimeField(default=timezone.now)
    img_avatar = models.ImageField(null=True)
    img_background = models.URLField(max_length=100, null=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, default=-900)

"""Book Model"""

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    anothername = models.CharField(max_length=200, null=True) 
    img = models.ImageField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    artist = models.CharField(max_length=100, null=True)
    isCompleted = models.BooleanField(null=True, blank=True)
    workerid = models.IntegerField(default=-1, null=True)
    note = models.TextField(null=True)
    quantityVol = models.IntegerField(default=0)
    dateUpload = models.DateField(null=True)
    dateUpdate = models.DateField(null=True)
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'anothername', 'author', 'artist', 'isCompleted', 'workerid', 'note', 'quantityVol', 'dateUpdate', 'dateUpload']


"""Category model"""

class Category(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=50)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id', 'name']