from django.contrib import admin	
from .models import BlogArticles	#将BogArticles 引入当前环境

class BlogArticlesAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "publish")
	list_filter = ("publish", "author")
	searh_fiels = ("title", "body")
	raw_id_fields = ("author", )
	date_hierarchy = "publish"
	ordering = ['publish', 'author']


admin.site.register(BlogArticles, BlogArticlesAdmin)	#将BlogArticles类和BlogArticlesAdmin类注册到admin中
