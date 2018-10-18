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
from django.conf.urls import include,url
#from django.urls import path,re_path,include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^pwd_reset/' ,include("password_reset.urls", namespace="pwd_reset", app_name="pwd_reset")),

    #path('admin/', admin.site.urls),
    #path('blog/', include('blog.urls')),
]
#如果在浏览器中输入类似http://localhost:8000/blog/的地址，通过该url配置，将请求转向到blog 应用的urls.py， 即./blog/urls.py
# 一般在./mysite/urls.py中配置URL后，在到某个应用中配置具体的urls.py
