from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from posts.models import Posts, Images
from posts.serializers import PostSerializer, ImagestSerializer
from rest_framework import pagination


class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    # Call Serializer class
    serializer_class = PostSerializer

    def get(self, request, format=None):
        objetcs = Posts.objects.all()
        serializer = PostSerializer(objetcs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImagesListCreateAPIView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    # Call Serializer class
    serializer_class = ImagestSerializer

    def get(self, request, format=None):
        objetcs = Images.objects.all()
        serializer = ImagestSerializer(objetcs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImagestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostsEditAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            object = Posts.objects.get(pk=kwargs['pk'])
            serializer = PostSerializer(object)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Posts.DoesNotExist:
            return Response(data={'message': "Not Page"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        objects = self.get_object()
        serializer = PostSerializer(objects, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'message': "Update Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        objects = self.get_object()
        if objects.id:
            Posts.objects.get(id=objects.id).delete()
            return Response(data={'message': "Delete Success"},
                        status=status.HTTP_204_NO_CONTENT)
        self.perform_destroy(objects)
        return Response(status=status.HTTP_204_NO_CONTENT)
