from django.urls import path, include
from users.views import  UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, ChangePasswordView
app_name = 'users'
urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="register"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('users/<key>/', UserTokenAPIView.as_view(), name="token"),
    path('users/reset/<str:pk>/',ChangePasswordView.as_view(),name="reset-password"),
]
