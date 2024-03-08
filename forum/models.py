# models.py

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    #content = models.TextField(verbose_name='Nội dung')
    content = RichTextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




class Comment(models.Model):
    post = models.ForeignKey('ForumPost', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)