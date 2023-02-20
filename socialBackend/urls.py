"""socialBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import stat
from django.contrib import admin
from django.urls import path, include
from authn.views import loginfunc, UserViewSet, signupFunc, forgotPassword
from postapp.views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from notifzz.views import NotificationViewSet
from chat.views import ChatViewSet, KeyRingViewSet

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")
router.register("post", PostViewSet, basename="post")
router.register("comment", CommentViewSet, basename="comment")
router.register("notification", NotificationViewSet, basename="notification")
router.register("chat", ChatViewSet, basename="chat")
router.register("keyring", KeyRingViewSet, basename="keyring")
urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api-auth/", include("rest_framework.urls")),
        path("login/", loginfunc, name="login"),
        path("signup/", signupFunc, name="signup"),
        path("forgot/", forgotPassword, name="forgot"),
        # path('',index),
        path("", include(router.urls)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
