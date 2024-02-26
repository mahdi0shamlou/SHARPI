from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index_home_section(request):
    return HttpResponse('<h1>Home section<h1>')