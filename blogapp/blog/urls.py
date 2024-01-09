from django.urls import path
from .views import PostListView, PostDetailView, create_post, add_comment_to_post

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', create_post, name='create_post'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
]