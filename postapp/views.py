import imp
from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializer import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.



class PostViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


