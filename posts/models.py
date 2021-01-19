from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class article(models.Model):
    author = models.EmailField()
    post_image = models.ImageField(upload_to='home/deepak/djangopro/mysite/Article/Freetalk/article_image',blank=True)
    article_title = models.TextField(max_length=80,blank=True)
    article_body = models.TextField(blank=True)
    tag = models.CharField(max_length=18)
    like = models.ManyToManyField(User, related_name="like", blank=True)
    post_created = models.DateTimeField(auto_now=True)

