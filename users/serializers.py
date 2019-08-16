from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from users.models import Image
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(read_only=True)
    avatar = serializers.ImageField(source='image.file',default='/photo.png')

    class Meta:
        model = User
        extra_kwargs = {'is_active': {'default': True}}
        fields = ('id', 'username', 'password', 'confirm_password','is_active','is_staff','is_superuser',
              'email', 'first_name', 'last_name', 'avatar')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        image = validated_data.pop('image')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        if image is not None:
            obj = Image(user=instance, **image)
            obj.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'old_password','new_password')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        return instance
