# models.py

from django.db import models
from django.contrib.auth.models import User
from app.models import UserInfo
from ckeditor.fields import RichTextField


class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


class Comment(models.Model):
    post = models.ForeignKey('ForumPost', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)