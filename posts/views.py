from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from postapp.models import Post
from .serializers import PostSerializer
# from .permissions import IsOwnerOrReadOnly


class PostAPIList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class PostAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (IsOwnerOrReadOnly, )