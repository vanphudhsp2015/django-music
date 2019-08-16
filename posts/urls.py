from django.urls import path, include
from posts.views import PostListCreateAPIView, PostsEditAPIView
app_name = 'posts'
urlpatterns = [
    path('posts/',include([
        path('', PostListCreateAPIView.as_view(), name="post-list"),
        path('<int:pk>/', PostsEditAPIView.as_view(), name="post-edit"),
    ])),
]

