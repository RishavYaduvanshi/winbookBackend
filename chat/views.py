from django.shortcuts import render
from rest_framework import (
    views,
    serializers,
    permissions,
    viewsets,
    decorators,
    response,
    pagination,
    status,
)
from . import serializers as chat_serializers, models
from django.http import HttpRequest
from django import shortcuts
from django.db.models import Q, F


class MessageViewSet(viewsets.ModelViewSet):
    class MessagePagination(pagination.PageNumberPagination):
        page_size = 10

    class MessageSerializer(serializers.ModelSerializer):
        from_user = serializers.SerializerMethodField()
        to_user = serializers.SerializerMethodField()

        message = serializers.SerializerMethodField()

        class Meta:
            model = models.Message
            fields = ["from_user", "to_user", "message", "created"]

        def get_from_user(self, obj):
            return {
                "name": obj.from_user.username,
                "dp": obj.from_user.dp.url,
                "pk": obj.from_user.pk,
            }

        def get_to_user(self, obj):
            return {
                "name": obj.to_user.username,
                "dp": obj.to_user.dp.url,
                "pk": obj.to_user.pk,
            }

        def get_message(self, obj):
            return obj.message or "sent an image"

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        return models.Message.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    @decorators.action(detail=False, methods=["get"])
    def get_chats(self, request: HttpRequest):
        # get all unique users with whom the current user has chatted

        chats = self.get_queryset().distinct("from_user", "to_user")
        page = self.paginate_queryset(chats)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return response.Response(self.MessageSerializer(chats, many=True).data)

    def retrieve(self, request, pk, *args, **kwargs):
        # get all messages between the current user and the user with the given pk
        messages = self.get_queryset().filter(Q(to_user=pk) | Q(from_user=pk))
        page = self.paginate_queryset(messages)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return response.Response(self.MessageSerializer(messages, many=True).data)

    def update(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        # delete message only if the current user is the sender
        message = shortcuts.get_object_or_404(
            models.Message, pk=kwargs["pk"], from_user=request.user
        )
        message.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
