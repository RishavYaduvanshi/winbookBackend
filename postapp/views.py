import imp
from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializer import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import Response, status
from rest_framework.decorators import action
from django.db.models import Q
# Create your views here.



class PostViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.pk
        
        
        serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        try:
            post = self.get_object()
            hasLiked = post.liked_by.filter(pk=request.user.pk).exists()
            
            if(not hasLiked):
                post.liked_by.add(request.user)
            else:
                post.liked_by.remove(request.user)
            
            post.save()
            return Response({"likes_count":post.liked_by.count(),"liked_status":not hasLiked},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, *args, **kwargs):
        if(self.get_object().user.pk==request.user.pk):
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if(self.get_object().user.pk==request.user.pk):
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    @action(methods=['get'], detail=False,url_path=r's/(?P<query>.+)')
    def search(self, request, query=None):

        posts = self.get_queryset().filter(Q(caption__icontains=query) | 
                Q(user__username__icontains=query) | Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)| Q(user__email__icontains=query))

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        if(self.get_object().user.pk==request.user.pk):
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)