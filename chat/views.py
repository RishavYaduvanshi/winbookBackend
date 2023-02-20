from django.shortcuts import render
from rest_framework import (
    views,
    serializers,
    viewsets,
    decorators,
    response,
    pagination,
    status,
)
from . import serializers, models
from rest_framework import permissions
from django.http import HttpRequest
from django import shortcuts


class ChatViewSet(viewsets.ModelViewSet):
    class ChatPagination(pagination.PageNumberPagination):
        page_size = 10

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ChatSerializer
    pagination_class = ChatPagination

    def get_queryset(self):
        return self.request.user.chats.all()

    @decorators.action(detail=True, methods=["get"])
    def get_messages(self, request, pk=None):
        chat = self.get_object()
        messages = chat.messages.all()

        result = serializers.MessageSerializer(
            self.paginate_queryset(messages), many=True
        )
        return self.get_paginated_response(result.data)

    def create(self, request: HttpRequest, *args, **kwargs):
        # add user to chat
        data = request.data.copy()
        print(data)
        users = data.getlist("users")

        if len(users) > 1:
            data.set("is_group", True)

        users.append(str(request.user.id))
        data.setlist("users", users)
        print(data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        if kwargs.get("partial", False):
            return super().update(request, *args, **kwargs)
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class KeyRingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.KeyRingSerializer

    def get_queryset(self):
        return shortcuts.get_object_or_404(models.KeyRing, user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        if kwargs.get("partial", False):
            return super().update(request, *args, **kwargs)
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return response.Response(
            serializers.KeyRingSerializer(self.get_queryset()).data
        )
