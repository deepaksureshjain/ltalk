from django.shortcuts import render
from django.http import JsonResponse
from .models import article
import json
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class PostArticle(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request):
        
       
        permission_classes = (IsAuthenticated)
        data = request.body.decode('utf8')
        data = json.loads(data)
        tok = data['token']
        user_name = Token.objects.get(key=tok).user
        if(user_name.is_authenticated==False):
            return(JsonResponse({'res':'LOGIN REQUIRED'},safe=False))
        if(len(data['title'])>3 and len(data['content'])>6):
            post = article(author=user_name, 
            article_title=data['title'],
            article_body=data['content'])
            post.save()
        else:
            return JsonResponse({'res':'Invalid post less content'})
        return JsonResponse({'res':'successfully created'},safe=False)
        
    


    def put(self,request,pk):
        permission_classes = (IsAuthenticated)
        post = article.objects.get(id=pk)
        token = request.META['HTTP_AUTHORIZATION']
        user_name = Token.objects.get(key=token).user
        user_id =user_name.id
        author = User.objects.get(username=post.author)

        if author.id == user_id: 
            data = request.body.decode('utf8')
            data = json.loads(data)
            try:
                for key in data:
                    if key == 'image':
                        post.post_image = data['image']
                    if key == 'article_title':
                        post.article_title =data['article_title']
                    if key == 'article_body':
                        post.article_body = data['article_body']
                post.save()
                return JsonResponse({'updated':'successfully updated'},safe=False)
            except:
                return JsonResponse({'error':'error in updating'},safe=False)
        else:
            return JsonResponse({'forbidden':'not allowed'},safe=False)       
    

    def delete(self,request,pk):
        permission_classes = (IsAuthenticated)
        post = article.objects.get(id=pk)
        token = request.META['HTTP_AUTHORIZATION']
        user_name = Token.objects.get(key=token).user
        user_id =user_name.id
        author = User.objects.get(username=post.author)
        if author.id == user_id:
            post.delete()
            return JsonResponse({'deleted':'successfully deleted'},safe=False)
        else:
            return JsonResponse({'forbidden':'not allowed'},safe=False)


class HomePage(View):

    def get(self, request):
        articles = {'articles': list(article.objects.values())}
        return JsonResponse(articles, safe=False)

def likepost(request,id):
    permission_classes = (IsAuthenticated)
    post = article.objects.get(id=id)
    token = request.META['HTTP_AUTHORIZATION']
    user = Token.objects.get(key=token).user
    post = post.like.add(user)
    post.save()

class ViewProfile(View):

    def get(self,request,username):
        profile = User.objects.get(username=username)
        articles = {'list':list(article.objects.filter(author=profile.username).values())}
        data = {}
        data['username'] = profile.username
        data['email'] = profile.email
        data['articles'] = list(article.objects.filter(author=profile.username).values())
        return JsonResponse(data,safe=False)
