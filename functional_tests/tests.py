from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest
import os
from lists.models import Item

class NewVisitorTest(StaticLiveServerTestCase):
    """ Тест нового посетителя"""

    def clear_items(self):
        items = Item.objects.all()
        for item in items:
            item.delete()
            
    def setUp(self):
        self.clear_items()
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """демонтаж """
        self.clear_items()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''подтверждение строки в таблице списка '''
        MAX_WAIT = 10
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
            time.sleep(0.5)

    def test_layout_and_styling(self):
        '''тест макета и стилевого оформления '''
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            266,
            delta = 10
            )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            266,
            delta = 10
            )

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно создать список и получить его позже"""

        #Теперь проверим, что наш сайт - это сайт со списком неотложных дел
        #открываем наш сайт
        self.browser.get(self.live_server_url)#'http:\\localhost:8000')

        #Проверяем, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
      
        #нам сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        #Мы набираем в текстовом поле "Купить кофе" (нельзя работать без кофе!)

        inputbox.send_keys('Buy a cup of coffee')
        
        #Когда мы нажимаем enter, страница обновляется, и теперь страница содержит
        #"1: Купить кофе" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1. Buy a cup of coffee')
        

        #Текстовое поле по-прежнему приглашает добавить еще один элемент
        #Мы вводим "выпить кофе" (не зря же покупали!)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink the cup of coffee')
        inputbox.send_keys(Keys.ENTER)

        #Страница снова обнавляется, и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table('1. Buy a cup of coffee')
        self.wait_for_row_in_list_table('2. Drink the cup of coffee')


#Нам интересно, запомнит ли сайт наш список.
#Здесь мы видим, что сайт сгенерировал для нас уникальный URL-адрес - об этом
#выводится небольшой текст с объяснениями
       # self.fail('Закончить тест')
#Мы посещаем этот URL-адрес - список по-прежнему там

#На этом можно завершать тест
    

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''тест: многочисленные пользователи могут начать списки по разным url'''
        #Начинаем новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a cup of coffee')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy a cup of coffee')

        #Замечаем, что список имеет уникальный URL адрес
        my_list_url = self.browser.current_url
        self.assertRegex(my_list_url, '/lists/.+')

        #Теперь новый пользователь, Френсис, приходит на сайт

        ##Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы
        ##никакая предыдущая информация не прошла через данные cookie

        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Френсис посещает домашнюю страницу. Нет никаких признаков списка
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a cup of coffee', page_text)
        self.assertNotIn('Drink the cup of coffee', page_text)

        #Френсис начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a bottle of milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy a bottle of milk')

        #Френсис получает уникальный URL адрес
        frencis_list_url = self.browser.current_url
        self.assertRegex(frencis_list_url, 'lists/.+')
        self.assertNotEqual(frencis_list_url, my_list_url)

        #Опять-таки, нет и следа первого списка
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a cup of coffee', page_text)
        self.assertIn('Buy a bottle of milk', page_text)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
