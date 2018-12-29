from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
# django 默认的用户登录两个方法
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserInfoForm  , UserForm

# 引用django 自带的模块
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
# Create your views here.
# 定义一个视图函数，处理前端提交的数据，须并支持前端的显示请求，第一个参数必为request


def user_login(request):
    if request.method == "POST":
        # 通过request.POST得到提交的表单数据，是一个类字典对象
        login_form = LoginForm(request.POST)
        # 验证传入的数据是否合法，
        if login_form.is_valid():
            # cd 以键值对形式记录用户密码 例cd = {'username':'admin', 'password' : '123456'}
            cd = login_form.cleaned_data
            # 用authenticate 检查该用户是否为本网站项目用户，以及密码是否正确，正确返回user对象，否在返回None
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                # 使用login方法，以user对象为参数，实现用户登录。用户登录之后，django会自动调用默认的session应用
                login(request, user)
                return HttpResponse("Welcome You. You have been authenticated successfully")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "registration/login.html", {"form": login_form})


def user_logout(request):
    return render(request, "account/logout.html")


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()  # 将表单数据保存到数据库

            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)  # 保存用户注册信息后，同时在account_userinfo数据库表中写入该用户ID
            # return HttpResponse("successfully")
            return HttpResponseRedirect(reverse_lazy("account:user_login"))
        else:
            return HttpResponse("Sorry, your can not register.")    # 这里也可以该为注册失败后的处理页面
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


def passwordChangeView(request):
    return render(request, "registration/password_change_form.html")


def passwordChangeDoneView(request):
    return render(request, "registration/password_change_done.html")


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


# 展示个人信息的视图函数
@login_required(login_url='/account/login/')  # django 自带装饰器，只有登录用户才能看自己信息
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)

    return render(request, "account/myself.html", {"user": user, "userinfo": userinfo,
                                                   "userprofile": userprofile})

# 编辑个人信息的视图函数


@login_required(login_url='/account/login/')  # 判断是否登录
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd["email"])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.school = userinfo_cd['company']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()

        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth,
                                                    "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                     "company": userinfo.company, "profession": userinfo.profession,
                                     "address": userinfo.address, "aboutme": userinfo.aboutme})

        return render(request, "account/myself_edit.html", {"user_form": user_form,
                                                            "userprofile_form": userprofile_form,
                                                            "userinfo_form": userinfo_form})


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html', )