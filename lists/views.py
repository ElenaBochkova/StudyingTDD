from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    '''Домашняя страница приложения Lists'''
    return HttpResponse('<html><title>To-Do lists</title></html>')
    
