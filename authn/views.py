import json
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
# Create your views here.


def loginfunc(request):
    if(not request.POST):
        request.POST = json.loads(request.body)
    
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)


    if(username is None or password is None):
        return  HttpResponse('{"status":"error","message":"username or password is empty"}',status=401)

    print(username,password)
    user = authenticate(username=username,password=password)

    if(user is None):
        return HttpResponse('{"status":"error","message":"username or password is wrong"}',status=401)
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return HttpResponse('{"status":"success","token":"'+token.key+'"}',status=200)


def signupFunc(request):
    # request.POST = json.loads(request.body)
    if(not request.POST):
        request.POST = json.loads(request.body)
    
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    first_name = request.POST.get('first_name',None)
    last_name = request.POST.get('last_name',None)
    email = request.POST.get('email',None)

    print(username,password,first_name,last_name,email)

    if( username is None or password is None or first_name is None or last_name is None or email is None):
        return HttpResponse('{"status":"error","message":"username or password is empty"}',status=401)

    else:
        user = User(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
    return HttpResponse('{"status":"success","message":"signup success"}',status=200)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    