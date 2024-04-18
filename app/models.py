from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from ckeditor.fields import RichTextField


# Create your models here.
# Change forms register django

"""User model"""

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
class UserInfo(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, primary_key=True)
    full_name = models.CharField(max_length=100, null=True)
    img_avatar = models.ImageField(upload_to='avatar_images/', null=True, default='avatar_images/default-avatar-profile-icon-of-social-media-user-vector.jpg')
    img_background = models.ImageField(upload_to='background_images/', null=True, blank=True)
    img_background_position = models.IntegerField(default=0)
    def __str__(self):
        return self.username.username

"""Category model"""

class Category(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=50)
    def __str__(self):
        return self.name

"""Book Model"""

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    anothername = models.CharField(max_length=200, null=True) 
    img = models.ImageField(upload_to='books_images/', null=True)
    author = models.CharField(max_length=100, null=True)
    artist = models.CharField(max_length=100, null=True)
    isCompleted = models.BooleanField(null=True, blank=True)
    workerid = models.IntegerField(default=-1, null=True)
    note = models.TextField(null=True)
    quantityVol = models.IntegerField(default=0)
    dateUpload = models.DateField(null=True)
    dateUpdate = models.DateTimeField(null=True)
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    isDeleted = models.BooleanField(default=False)
    def __str__(self):
        return self.title

"""Volumes"""

class Volume(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, related_name='volumes', on_delete=models.CASCADE)
    title = models.TextField()
    img = models.ImageField(upload_to='volume_images/')
    def __str__(self):
        return self.title

"""Chapters"""

class Chapter(models.Model):
    id = models.AutoField(primary_key=True,)
    volume = models.ForeignKey(Volume, related_name='chapters', on_delete=models.CASCADE)
    title = models.TextField(default='')
    content = RichTextField(default='')
    view = models.IntegerField(default=0)
    date_upload = models.DateTimeField(null=True, blank=True)

    def increase_views(self):
        self.view += 1  
        self.save()  

    def __str__(self):
        return str(self.id)

class ChapterComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments', null=True, blank=True)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='chapter_comments', null=True, blank=True)
    content = models.TextField()
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
class ChapterCommentForm(forms.ModelForm):
    class Meta:
        model = ChapterComment
        fields = ['content']
        labels = {'content': ''}
        error_messages = {
            'content': {
                'required': 'Nhập nội dung bình luận',
            }
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'style': 'width:100%;'}),
        }
        
"""Book Following"""
class BookFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} is following {self.book.title}"

"""Translate Group"""

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=40, db_index=True)
    description = models.TextField(null=True, blank=True, default="Chào mừng bạn xem group chúng tôi")
    
    def __str__(self) -> str:
        return self.groupname  
     
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupname']
        
class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['description']
    
class Member(models.Model):
    auth_user = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE)  
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    teamrole = models.CharField(max_length=40, db_index=True, default="Thành viên")

    def __str__(self):
        return f'{self.auth_user.username}  (gr: {self.group.groupname}| {self.teamrole})'


