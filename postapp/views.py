from django.db import IntegrityError
from rest_framework import viewsets
from .models import Post, Comment
from .serializer import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import Response, status
from rest_framework.decorators import action
from django.db.models import Q
from django.http import HttpRequest, Http404
from django.apps import apps

UserModel = apps.get_model("authn", "User")


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.pk

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except IntegrityError as e:
            if "url_or_caption" in str(e):
                return Response(
                    {"error": "Image and/or Caption Required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(methods=["get"], detail=False)
    def feed(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_anonymous:
            return Http404()

        queryset = self.queryset.filter(
            Q(user__in=request.user.followers.all())
            | Q(user__in=request.user.following.all())
            | Q(user=request.user)
        ).order_by("-created_at")

        # handled if the user has no followers and following
        if queryset.count() == 0:
            queryset = UserModel.objects.filter(username="admin").first().posts.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        try:
            post = self.get_object()
            post.toggle_like(request.user)

            return Response(
                {
                    "likes_count": post.liked_by.count(),
                    "liked_status": post.liked_by.filter(
                        pk=self.request.user.pk
                    ).exists(),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

    def destroy(self, request, *args, **kwargs):
        if self.get_object().user.pk == request.user.pk:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if self.get_object().user.pk == request.user.pk:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=["get"], detail=False, url_path=r"s/(?P<query>.+)")
    def search(self, request, query=None):

        posts = self.get_queryset().filter(
            Q(caption__icontains=query)
            | Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
        )

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        if self.get_object().user.pk == request.user.pk:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=["get"], detail=True)
    def get_comments(self, request, pk=None):
        post = self.get_object()
        return Response(CommentSerializer(post.comments.all(), many=True).data)

    @action(methods=["post"], detail=True)
    def comment(self, request, pk=None):
        post = self.get_object()
        data = request.data.copy()
        data["user"] = request.user.pk
        data["post"] = post.pk
        data["replied_to"] = None
        print(data)
        serializer = CommentSerializer(data=data, write=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(methods=["post"], detail=True)
    def reply(self, request, pk=None):

        if self.request.user.is_anonymous:
            return Response(
                status=status.HTTP_403_FORBIDDEN, data={"error": "Not logged in"}
            )

        comment = self.get_object()
        data = request.data.copy()
        data["user"] = request.user.pk
        data["replied_to"] = comment.pk
        print(data)
        serializer = CommentSerializer(data=data, write=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=True)
    def get_replies(self, request, pk=None):
        comment = self.get_object()
        return Response(CommentSerializer(comment.replies.all(), many=True).data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer([instance], many=True)
        print(serializer.data)
        return Response(serializer.data)
