from django import forms
from .models import ForumPost

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        labels = {
            'title': 'Tiêu đề',
            'content': 'Nội dung',
        }
