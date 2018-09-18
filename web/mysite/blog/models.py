from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class BlogArticles(models.Model):
    title = models.CharField(max_length=30) #定义Char类型的title字段最大长度30
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)   #通过FeignKey 规定博客文章和用户之间的关系--一个用户对应多篇文章
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)    #按照publish的倒序排序
    
    def __str__(self):
        return self.title



