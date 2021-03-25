from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Question

# 向管理页面注册了问题 Question 类
admin.site.register(Question)
# admin.site.register(Question)
