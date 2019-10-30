from rest_framework import serializers
from posts.models import Posts, Images

class PostSerializer(serializers.ModelSerializer):

  class Meta:
        model = Posts
        fields = '__all__'

class ImagestSerializer(serializers.ModelSerializer):

  class Meta:
        model = Images
        fields = '__all__'
