import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.base import TemplateResponseMixin
from .models import Course, Lesson
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin

# Post请求类相关
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from .forms import CreateCourseForm, CreateLessonForm


class AboutView(TemplateView):
    template_name = "course/about.html"


# ListView读取数据
class CourseListView(ListView):  # 继承ListView类用于保存数据
    model = Course  # 声明本类用到的数据模型  相当于之前使用视图函数时候的Course.object.all()
    # queryset = Course.objects.filter(user=User.objects.filter(username="test"))
    context_object_name = "courses"  # 声明传入模板中的变量名称（如果不写则模板默认变量名称为"object"）
    template_name = 'course/course_list.html'  # 声明模板文件

    # def get_queryset(self):
    #     qs = super(CourseListView, self).get_queryset()
    #     return qs.filter(user=User.objects.filter(username="immt"))


class UserMixin:  # Mixin类申明，表示这个类将用于后面的类的多继承中
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


# class UserCourseMixin(UserMixin):
#     model = Course

class UserCourseMixin(UserMixin, LoginRequiredMixin):
    # 用多重继承Mixin 的方法 实现判断用户是否登录
    model = Course
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


# 创建数据 CreateView
class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form": form})


# 删除数据 deleteView
class DeleteCourseView(UserCourseMixin, DeleteView):
    template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


# 编辑数据 updateView 还未实现
class UpdateViewCourseView(UserCourseMixin, UpdateView):
    template_name = 'course/manage/update_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")


# 课程内容视图
class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login/"

    def get(self, request, *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request, "course/manage/create_lesson.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


# 查看课程内容
class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course': course})


class DetailLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return self.render_to_response({"lesson": lesson})


class StudentListLessonView(ListLessonsView):
    template_name = "course/slist_lessons.html"

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.student.add(self.request.user)
        return HttpResponse("ok")
