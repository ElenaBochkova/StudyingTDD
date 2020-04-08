from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

# Create your views here.

def home_page(request):
    '''Домашняя страница приложения Lists'''
    #if request.method == 'POST':
     #   Item.objects.create(text=request.POST['item_text'])
     #   return redirect('lists/one_in_the_world_list')

   # items = Item.objects.all()
    return render(request, 'lists/home.html')#, {'items': items})

def view_list(request, list_id):
    '''представление списка'''
    list_ = List.objects.get(id = list_id)
    items = Item.objects.filter(my_list=list_)
    return render(request, 'lists/list.html', {'list': list_})

def new_list(request):
    '''новый список '''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], my_list = list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    '''добавить элемент '''
    list_ = List.objects.get(id = list_id)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    ''' добавить элемент'''
    list_ = List.objects.get(id = list_id)
    Item.objects.create(text = request.POST['item_text'], my_list = list_)
    return redirect(f'/lists/{list_.id}/')
    
