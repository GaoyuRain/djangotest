"""
author :rain
Date : 2021/03/17
Description :
"""

from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello world ! ")


