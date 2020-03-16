from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page


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
