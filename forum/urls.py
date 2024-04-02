# urls.py

from django.urls import path
from .views import PostListView, PostDetailView, CreatePostView, add_comment_to_post
from django.conf.urls import include


urlpatterns = [
    path('posts/', PostListView.as_view(), name='forum-post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', CreatePostView, name='create-post'),
    path('posts/<int:post_id>/comment/', add_comment_to_post, name='add-comment-to-post'),
]