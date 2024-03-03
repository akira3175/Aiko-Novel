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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
