from django.urls import path
from .views import PostListView, PostDetailView, CreatePostView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='forum-post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', CreatePostView, name='create-post'),
]