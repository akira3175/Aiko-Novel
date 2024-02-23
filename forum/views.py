from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import ForumPost
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import ForumPostForm

from django.contrib.auth.models import User

# hien thi danh sach bai dang theo thu tu som nhat
class PostListView(ListView):
    model = ForumPost
    template_name = 'forum/forum_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return ForumPost.objects.all().order_by('-created_at')

# chi tiet noi dung bai dang; comment cua bai dang hien thi theo thu tu som nhat
class PostDetailView(DetailView):
    model = ForumPost
    template_name = 'forum/forum_post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        return context
    

# tao bai dang moi
@login_required
def CreatePostView(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            return redirect('/forum/posts')
        else:
            print(form.errors)
    else:
        form = ForumPostForm()

    return render(request, 'forum/create_post.html', {'form': form})
