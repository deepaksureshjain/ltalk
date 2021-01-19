from django.shortcuts import render
from django.views import View
import json
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from posts.models import article
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
#from .models import Account


# Create your views here.
class UserRegister(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        data = request.body.decode('utf8')
        data = json.loads(data)
        try:
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({'error': 'username exists'}, safe=False, status=200)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'email id exists'}, safe=False, status=400)
            else:
                if len(data['username'])<=5:
                    return JsonResponse({'error':'invalid username'})
                if len(data['password1'])<8:
                    return JsonResponse({'error':"invalid password"})
                if data['password1'] != data['password2']:
                    return JsonResponse({'error':'password not match'},safe=False,status=200)
                else:
                    user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password1'])
                    user.save()
                    token = Token.objects.get(user=user).key
                    response={}
                    response['token'] = token
                    response['success'] ='successfully created'
                    auth.login(request,user)
                    return JsonResponse(response,safe=False)
        except:
            return JsonResponse({'error': 'something went wrong'}, safe=False, status=400)


class SignIn(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self,request):
        data = request.body.decode('utf8')
        data = json.loads(data)
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                token = Token.objects.get(user=user).key
                response = {}
                response['token'] = token
                print(token)
                response['success'] ='successfully created'
                return JsonResponse(response,safe=False)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, safe=False)
        else:
            return JsonResponse({'error': 'user not exists'}, safe=False)


def logout(request):
    auth.logout(request)
    return JsonResponse({'success':'succesfully signed out'},safe=False,)

class EditProfile(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def post(self,request):
        permission_classes = (IsAuthenticated)
        data =  request.body.decode('utf8')
        data = json.load(data)
        token = request.META['HTTP_AUTHORIZATION']
        user_name = Token.objects.get(key=token).user
        user = User.objects.get(username=user_name)
        for key in data:
            if key == "newpassword":
                if user.password == data['oldpasword']:
                    user.password = data['newpassword']
                    user.save()
                    return JsonResponse({'updated':'password updated'},safe=False)
                else:
                    return JsonResponse({'error': 'password incorrect'}, safe=False, status=400)
            if key == "email":
                user.email = data['email']
                user.save()
                return JsonResponse({'updated':'email id updated'},safe=False)

class MyAccount(View):
    def get(self,request):
        
        tok=request.META['HTTP_AUTHORIZATION']
        print(tok)
        token_user_name = Token.objects.get(key=tok).user
        print(tok,token_user_name)
        data = {}
        user = User.objects.get(username = token_user_name)
        if article.objects.filter(author=token_user_name).exists():
            articles = {'articles': list(article.objects.filter(author=token_user_name).values())}
            data['article'] = articles
        else:
            data['article'] = None

        data['username'] = user.username
        data['email'] = user.email
        return JsonResponse(data,safe=False)
