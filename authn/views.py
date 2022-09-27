import json
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.views import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Q
from django.core.mail import send_mail
from .helpers import forgot_password
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

# Create your views here.


def loginfunc(request):
    if not request.POST:
        request.POST = json.loads(request.body)

    username = request.POST.get("username", None)
    password = request.POST.get("password", None)

    if username is None or password is None:
        return HttpResponse(
            '{"status":"error","message":"username or password is empty"}', status=401
        )

    print(username, password)
    user = authenticate(username=username, password=password)

    if user is None:
        return HttpResponse(
            '{"status":"error","message":"username or password is wrong"}', status=401
        )
    else:
        token, _ = Token.objects.get_or_create(user=user)
        return HttpResponse(
            '{"status":"success","token":"' + token.key + '"}', status=200
        )


def signupFunc(request):
    # request.POST = json.loads(request.body)
    if not request.POST:
        request.POST = json.loads(request.body)

    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    first_name = request.POST.get("first_name", None)
    last_name = request.POST.get("last_name", None)
    email = request.POST.get("email", None)

    print(username, password, first_name, last_name, email)

    if (
        username is None
        or password is None
        or first_name is None
        or last_name is None
        or email is None
    ):
        return HttpResponse(
            '{"status":"error","message":"username or password is empty"}', status=401
        )

    else:
        user = User(
            username=username, first_name=first_name, last_name=last_name, email=email
        )
        user.set_password(password)
        user.save()
    return HttpResponse('{"status":"success","message":"signup success"}', status=200)


def forgotPassword(request):
    if not request.POST:
        request.POST = json.loads(request.body)

    email = request.POST.get("email", None)
    token = request.POST.get("token", None)
    if email is None:
        return HttpResponse('{"status":"error","message":"email is empty"}', status=401)
    else:
        user = User.objects.filter(email=email)
        if user.exists():
            user = user[0]
            if token is None:
                send_mail(
                    subject="Reset Password",
                    html_message=forgot_password.gen_forgot_mail(request, user),
                    message="",
                    from_email="no-reply@winbook.gg",
                    fail_silently=False,
                    recipient_list=[user.email],
                )
                return HttpResponse(
                    '{"status":"success","message":"email sent"}', status=200
                )
            else:
                password = request.POST.get("password", None)
                if password is None:
                    return HttpResponse(
                        '{"status":"error","message":"password is empty"}', status=401
                    )

                if forgot_password.verify_forgot_token(user, token):
                    user.set_password(password)
                    user.save()
                    logoutFromAll = bool(request.POST.get("logout", False))
                    if logoutFromAll:
                        Token.objects.filter(user=user).delete()
                    return HttpResponse(
                        '{"status":"success","message":"password changed"}', status=200
                    )
                else:
                    return HttpResponse(
                        '{"status":"error","message":"token is invalid"}', status=401
                    )
        else:
            return HttpResponse(
                '{"status":"error","message":"email is invalid"}', status=401
            )


class UserViewSet(ModelViewSet):
    class UserPaginator(PageNumberPagination):
        page_size = 10

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPaginator

    def create(self, request, *args, **kwargs):
        return Response(
            {"status": "error", "message": "you are not allowed to create users"},
            status=401,
        )

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.pk == self.get_object().pk:
            return super().update(request, *args, **kwargs)
        return Response(
            {"status": "error", "message": "you are not allowed to update this user"},
            status=401,
        )

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.pk == self.get_object().pk:
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"status": "error", "message": "you are not allowed to delete this user"},
            status=401,
        )

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.pk == self.get_object().pk:
            partial = True
            instance = get_object_or_404(User, pk=request.user.pk)
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(
            {"status": "error", "message": "you are not allowed to update this user"},
            status=401,
        )

    @action(detail=True, methods=["post", "delete"])
    def update_dp(self, request, *args, **kwargs):
        if request.method.lower() == "delete":
            user = self.get_object()
            user.dp = "../static/authn/dp.png"
            user.save()
            return Response({"status": "success", "message": "dp deleted"})

        pk = kwargs["pk"]
        if request.user.is_superuser or request.user.pk == self.get_object().pk:
            instance = get_object_or_404(User, pk=pk)
            instance.dp = request.data["dp"]
            instance.save()
            return Response({"status": "success", "message": "dp updated successfully"})

        return Response(
            {"status": "error", "message": "you are not allowed to update this user"},
            status=401,
        )

    @action(detail=True, methods=["post", "delete"])
    def update_cover(self, request, *args, **kwargs):
        if request.method.lower() == "delete":
            user = self.get_object()
            user.cover = "../static/authn/cover.png"
            user.save()
            return Response({"status": "success", "message": "cover deleted"})

        pk = kwargs["pk"]

        if request.user.is_superuser or request.user.pk == self.get_object().pk:
            instance = get_object_or_404(User, pk=pk)
            instance.cover = request.data["cover"]
            instance.save()
            return Response(
                {"status": "success", "message": "cover updated successfully"}
            )

        return Response(
            {"status": "error", "message": "you are not allowed to update this user"},
            status=401,
        )

    @action(detail=False, methods=["get", "post"], url_path=r"f/(?P<username>.+)")
    def get_by_username(self, request, *args, **kwargs):
        query = kwargs.get("username", None)
        follow = request.POST.get("follow", None)
        if query is None:
            return Response(
                {"status": "error", "message": "username is empty"}, status=400
            )
        print(query)
        instance = get_object_or_404(User, username=query)

        if request.user.is_authenticated and (follow is not None):
            follow = True if follow.lower() == "true" else False
            print(follow)
            if follow:
                request.user.follow(instance)
            else:
                request.user.unfollow(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"s/(?P<query>.+)")
    def search(self, request, *args, **kwargs):
        query = kwargs["query"]
        print(query)
        instance = User.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )
        serializer = self.get_serializer(self.paginate_queryset(instance), many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"])
    def followers(self, request, *args, **kwargs):
        class FollowerSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ["username", "first_name", "last_name", "dp"]

        instance = self.get_object()
        serializer = FollowerSerializer(
            self.paginate_queryset(instance.followers.all()), many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, *args, **kwargs):
        class FollowingSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ["username", "first_name", "last_name", "dp"]

        instance = self.get_object()
        serializer = FollowingSerializer(
            self.paginate_queryset(instance.following.all()), many=True
        )
        return self.get_paginated_response(serializer.data)
