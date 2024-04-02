# form.py

from django import forms
from .models import ForumPost, Comment

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        labels = {
            'title': 'Tiêu đề',
            'content': 'Nội dung',
        }
        error_messages = {
            'title': {
                'required': 'Nhập tiêu đề bài đăng',
            },
            'content': {
                'required': 'Nhập nội dung bài đăng',
            }
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        error_messages = {
            'content': {
                'required': 'Nhập nội dung bình luận',
            }
        }
        
