from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from users.serializers import  UserRegistrationSerializer, UserLoginSerializer, TokenSerializer, ChangePasswordSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from users.models import AvatarUser
from django.contrib.auth.decorators import login_required

class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key
        data['avatar'] = '/media/photo.png'

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

# Login View Json
class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            userObject = User.objects.filter(username=user)
            serializer = UserRegistrationSerializer(userObject, many = True)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'auth_token':token.key,
                    "date":token.created,
                    "users":serializer.data
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

# Logout
class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            serializer = self.get_serializer(data=request.data)
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "delete":
            data = [{"message":"logout success"}]
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)

class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        permission_classes = (AllowAny,)
        serializer_class = ChangePasswordSerializer
        model = User

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
