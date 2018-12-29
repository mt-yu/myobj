# django 的自定义模板标签
from django.utils.safestring import mark_safe
import markdown
from django import template
from article.models import ArticlePost
from django.db.models import Count


register = template.Library()


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles": latest_articles}


@register.simple_tag    # 取消了 assignment_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]

#  自定义个过滤器 将markdown 文本 转换为 html 文本
@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))

