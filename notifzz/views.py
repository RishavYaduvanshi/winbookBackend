from django.shortcuts import render
from rest_framework import viewsets
from .models import Notification
from rest_framework import serializers
from postapp.serializer import PostSerializer
from authn.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    class NotificationPagination(PageNumberPagination):
        page_size = 10

    class NotificationSerializer(serializers.ModelSerializer):

        post = PostSerializer()
        actor = UserSerializer()

        class Meta:
            model = Notification
            exclude = ["users"]

    serializer_class = NotificationSerializer

    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(users=self.request.user)

    @action(detail=False, methods=["get"])
    def unread(self, request):
        return self.get_queryset().filter(isRead=False)
