# views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import ForumPost
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import ForumPostForm, CommentForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin

# hien thi danh sach bai dang theo thu tu som nhat
class PostListView(ListView):
    model = ForumPost
    template_name = 'forum/forum_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return ForumPost.objects.all().order_by('-created_at')

# chi tiet noi dung bai dang; comment cua bai dang hien thi theo thu tu som nhat va hien ra form de binh luan
class PostDetailView(FormMixin, DetailView):
    model = ForumPost
    template_name = 'forum/forum_post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        context['comment_form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.username = self.request.user
        comment.save()
        return super().form_valid(form)


# tao bai dang moi
@login_required
def CreatePostView(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            return redirect('forum-post-list')
        else:
            print(form.errors)
    else:
        form = ForumPostForm()

    return render(request, 'forum/create_post.html', {'form': form})

@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.username = request.user
            comment.save()
            return redirect('post-detail', pk=post_id)
    else:
        form = CommentForm()

    return render(request, 'forum/forum_post_detail.html', {'comment_form': form, 'post': post})