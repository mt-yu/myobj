from django.conf.urls import url
from django.urls import path
#引入Django内置视图文件，
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

app_name='account'

urlpatterns = [
    #views.user_login 意味着必须在views中创建一个名为user_login的函数响应请求
    #url(r'^login/$', views.user_login, name="user_login"),  #自定义的登录

    url(r'^login/$', auth_views.LoginView.as_view(), name="user_login"),  #django内置的登录
    url(r'^new-login/$', auth_views.LoginView.as_view(), {"template_name": "account/login.html"}),  #修改template_name 属性的值，使用account/login.html

    #url(r'^logout/$', auth_views.LogoutView.as_view(), name="user_logout"), #内置django退出登录
    #path('logout/', auth_views.LogoutView.as_view(),{"template_name": "account/login.html"},name='user_logout')
    url(r'^logout/$', auth_views.LogoutView.as_view(), {"template_name" :"account/logout.html"}, name="user_logout"),
]
