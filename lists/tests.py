from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

import time

from lists.views import home_page
from .models import Item, List


class HomePageTest(TestCase):
    """ тест домашней страницы"""

    def test_root_url_resolves_to_home_page_view(self):
        ''' тест: корневой url преобразуется в представление домашней страницы'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''тест: домашняя страница использует нужный шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элементов списка'''
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.my_list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.my_list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.my_list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.my_list, list_)

class ListViewTest(TestCase):
    '''тест представления списка'''
    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')
    
    def test_displays_only_items_for_that_list(self):
        ''' тест: отображаются все элементы списка'''
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', my_list = correct_list)
        Item.objects.create(text='itemey 2', my_list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text = 'other 1 item', my_list = other_list)
        Item.objects.create(text = 'other 2 item', my_list = other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other 1 item')
        self.assertNotContains(response, 'other 2 item')

class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить POST запрос '''
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''тест: переадресует после POST запроса'''
        response = self.client.post('/lists/new', data={'item_text':
                                                        'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class BewItemTest(TestCase):
    '''тест нового элемента списка'''

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест: можно сохранить post-запрос в существующий список '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
            )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.my_list, correct_list)

    def test_redirects_to_list_view(self):
        '''тест: переадресуется в представление списка '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
            )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_passes_correct_list_to_template(self):
        '''тест: передается правильный шаблон списка '''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
