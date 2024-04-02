from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


# Create your models here.
# Change forms register django

"""User model"""

class Role(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=200, null=False, blank=False)
    def __str__(self):
        return self.role_name

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
class UserInfo(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, primary_key=True)
    full_name = models.CharField(max_length=100, null=True)
    date_join = models.DateTimeField(default=timezone.now)
    img_avatar = models.ImageField(upload_to='avatar_images/', null=True)
    img_background = models.ImageField(upload_to='background_images/', null=True, blank=True)
    img_background_position = models.IntegerField(default=0)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, default=-999)
    def __str__(self):
        return self.username.username

class UserInfoForm(forms.ModelForm):
    """role_id = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)"""
    class Meta:
        model = UserInfo
        fields = ['username', 'full_name', 'date_join', 'img_avatar', 'img_background'] 

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
    category = models.CharField(max_length=100, null=True) 
    def __str__(self):
        return self.title

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'anothername', 'author', 'artist', 'isCompleted', 'workerid', 'note', 'quantityVol', 'dateUpdate', 'dateUpload']


"""Category model"""

class Category(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=50)
    def __str__(self):
        return self.name

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id', 'name']

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=40, db_index=True)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


