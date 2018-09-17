from django.shortcuts import render, get_object_or_404
from .models import BlogArticles

# Create your views here.

#查看文章标题的函数
def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs":blogs})

#查看文章详情请求的函数
def blog_article(request, article_id):
    #article = BlogArticles.objects.get(id = article_id)
    #get_object_or_404 类似 try expect中 使用 raise Http404（）
    article = get_object_or_404(BlogArticles, id = article_id)
    pub = article.publish
    return render(request, "blog/content.html", {"article":article, "publish":pub})
