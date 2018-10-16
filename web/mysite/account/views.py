from django.shortcuts import render

from django.http import HttpResponse
#django 默认的用户登录两个方法
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm

#引用django 自带的模块
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

# Create your views here.
#定义一个视图函数，处理前端提交的数据，并支持前端的显示请求，第一个参数必须为request
def user_login(request):
    if request.method == "POST":
        #通过request.POST得到提交的表单数据，是一个类字典对象
        login_form = LoginForm(request.POST)
        #验证传入的数据是否合法，
        if login_form.is_valid():
            #cd 以键值对形式记录用户密码 例cd = {'username':'admin', 'password' : '123456'}
            cd = login_form.cleaned_data
            #用authenticate 检查该用户是否为本网站项目用户，以及密码是否正确，正确返回user对象，否在返回None
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                #使用login方法，以user对象为参数，实现用户登录。用户登录之后，django会自动调用默认的session应用
                login(request, user)
                return HttpResponse("Wellcome You. You have been authenticated successfully")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form":login_form})

def user_logout(request):
    return render(request, "account/logout.html")

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()

            return HttpResponse("successfully")
        else:
            return HttpResponse("Sorry, your can not register.")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form" : user_form, "profile" : userprofile_form})


def passwordChangeView(request):
    return render(request, "account/password_change_form.html")

def passwordChangeDoneView(request):
    return render(request, "account/password_change_done.html")

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


