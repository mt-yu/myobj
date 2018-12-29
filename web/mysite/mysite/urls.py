"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView  # 引入通用视图
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('blog/', include('blog.urls')),
    #path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace='account')),
    path('article/', include('article.urls', namespace='article')),
    path('home/', TemplateView.as_view(template_name="home.html"), name='home'),
    path('image/', include('image.urls', namespace='image')),
    path('course/', include('course.urls', namespace='course')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 如果在浏览器中输入类似http://localhost:8000/blog/的地址，通过该url配置，将请求转向到blog 应用的urls.py， 即./blog/urls.py
# 一般在./mysite/urls.py中配置URL后，在到某个应用中配置具体的urls.py
