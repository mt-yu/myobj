from django import forms
from django.contrib.auth.models import User  # 引入用户默认的User模型,不需要用户新建数据模型
from .models import UserProfile, UserInfo


# 用户登录表单
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=5)


# 用户注册表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = {"username", "email"}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {"email", }    # 不要加入 username // username 注册之后不允许修改
