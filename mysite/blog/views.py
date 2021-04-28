from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from pprint import pprint


def index(request):
    return HttpResponse('Hello again django nube. I missed you!')


def get_blogs(request):
    pprint(data)
    blogs = Blog.objects.all()

    return HttpResponse([{'blogname': b.name} for b in blogs])

