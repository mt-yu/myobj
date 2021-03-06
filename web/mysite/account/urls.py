from django.conf.urls import url
from django.urls import path, re_path
# 引入Django内置视图文件，
from django.contrib.auth import views as auth_views  # 输入内置的账户管理视图模块
from . import views
# from django.conf import settings
from django.urls import reverse_lazy

app_name = 'account'

urlpatterns = [
    # views.user_login 意味着必须在views中创建一个名为user_login的函数响应请求
    # url(r'^login/$', views.user_login, name="user_login"),  #自定义的登录

    # """ 登录 """
    # django内置的登录
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name="user_login"),
    # #修改template_name 属性的值，使用account/login.html


    # """ 退出登录 """
    # 使用函数的形式
    # url(r'^logout/$', views.user_logout, name="user_logout"),
    # 内置django退出登录
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),


    # """ 注册 """
    url(r'^register/$', views.register, name="user_register"),


    # """ 修改密码 """
    # url(r'^password-change/$', views.passwordChangeView, name="password_change"),
    re_path(r'^password-change/$',
            auth_views.PasswordChangeView.as_view(
                success_url=reverse_lazy('account:password_change_done'),
                template_name='registration/password_change_form.html'),
            name="password_change"),
    # url(r'^password-change/$', auth_views.PasswordChangeView.as_view(), name="password_change"),
    # url(r'^password-change-done/$', views.passwordChangeDoneView, name="password_change_done"),
    url(r'^password-change-done/$',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'),
        name='password_change_done'),


    # """ 重置密码 """
    url(r'^password-reset/$',
        auth_views.PasswordResetView.as_view(
            email_template_name="registration/password_reset_email.html",
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('account:password_reset_done'),
            template_name="registration/password_reset_form.html"),
        name='password_reset'),

    re_path(r'^password-reset-done/$',
            auth_views.PasswordResetDoneView.as_view(
                template_name="registration/password_reset_done.html"),
            name='password_reset_done'),

    re_path(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name="registration/password_reset_confirm.html",
                success_url = "/account/password-reset-complete"),
            name='password_reset_confirm'),

    re_path(r'^password-reset-complete',
            auth_views.PasswordResetCompleteView.as_view(
                template_name="registration/password_reset_complete.html"),
            name='password_reset_complete'),

    # """ 个人信息 """
    re_path(r'^my-information/$', views.myself, name="my_information"),
    re_path(r'^edit-my-information/$', views.myself_edit, name="edit_my_information"),
    re_path(r'^my-image/$', views.my_image, name="my_image"),
]
