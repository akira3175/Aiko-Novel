from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


# Create your models here.
# Change forms register django

"""User model"""

class Role(models.Model):
    role_id = models.IntegerField(primary_key=True, default=-900)
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
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.username.username

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'full_name', 'date_join', 'img_avatar', 'img_background'] 

"""Book Model"""

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    anothername = models.CharField(max_length=200, null=True) 
    img = models.ImageField(upload_to='books_images/', null=True)
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

"""Category-Book model"""

class CategoryBook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.book.title} - {self.category.name}"
    
class CategoryBookForm(forms.ModelForm):
    class Meta:
        model = CategoryBook
        fields = '__all__'

"""Translate Group"""

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=40, db_index=True)
    
    def __str__(self) -> str:
        return self.groupname  
     
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupname']

    
class Member(models.Model):
    auth_user = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE)  
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    teamrole = models.CharField(max_length=40, db_index=True, default="member")

    def __str__(self):
        return f'{self.auth_user.username}  (gr: {self.group.groupname})'


