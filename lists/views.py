from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

# Create your views here.

def home_page(request):
    '''Домашняя страница приложения Lists'''
    #if request.method == 'POST':
     #   Item.objects.create(text=request.POST['item_text'])
     #   return redirect('lists/one_in_the_world_list')

   # items = Item.objects.all()
    return render(request, 'lists/home.html')#, {'items': items})

def view_list(request):
    '''представление списка'''
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    '''новый список '''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/one_in_the_world_list/')
    
