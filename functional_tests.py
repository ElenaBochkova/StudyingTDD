from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    """ Тест нового посетителя"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """демонтаж """
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно создать список и получить его позже"""

        #Теперь проверим, что наш сайт - это сайт со списком неотложных дел
        #открываем наш сайт
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1. Buy a cup of coffee', [row.text for row in rows])
        

        #Текстовое поле по-прежнему приглашает добавить еще один элемент
        #Мы вводим "выпить кофе" (не зря же покупали!)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink the cup of coffee')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #Страница снова обнавляется, и теперь показывает оба элемента списка
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1. Buy a cup of coffee', [row.text for row in rows])
        self.assertIn('1. Drink the cup of coffee', [row.text for row in rows])

#Нам интересно, запомнит ли сайт наш список.
#Здесь мы видим, что сайт сгенерировал для нас уникальный URL-адрес - об этом
#выводится небольшой текст с объяснениями
        self.fail('Закончить тест')
#Мы посещаем этот URL-адрес - список по-прежнему там

#На этом можно завершать тест


if __name__ == '__main__':
    unittest.main(warnings='ignore')
