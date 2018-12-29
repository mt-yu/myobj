from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify


class ArticleColumn(models.Model):
    
    user = models.ForeignKey(User, related_name='article_column', on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name="tag", on_delete=models.CASCADE)
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)
    class Meta:
        ordering = ("-updated",)   # 按照某字段进行排列(这里是按照文章更新时间倒序)
        index_together = (('id', 'slug'),)  # 对数据库中的该两字段建立索引 可以提高读取文章的速度

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):  # 每个数据模型都提供了save方法，这里对其进行重写
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])  # reverse(函数获得对应的URL)

    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])


# 评论相关
class Comment(models.Model):
    # article 字段 使的本数据模型与ArticlePost建立关系属于多对一关系
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)    # 按照创建时间逆排序

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)

