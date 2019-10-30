from django.urls import path, include
from posts.views import PostListCreateAPIView, PostsEditAPIView, ImagesListCreateAPIView
app_name = 'posts'
urlpatterns = [
    path('images/',include([
        path('', ImagesListCreateAPIView.as_view(), name="images-list")
    ])),
]

