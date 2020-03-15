from selenium import webdriver
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
        self.fail('Закончить тест')

#нам сразу же предлагается ввести элемент списка

#Мы набираем в текстовом поле "Купить кофе" (нельзя работать без кофе!)

#Когда мы нажимаем enter, страница обновляется, и теперь страница содержит
#"1: Купить кофе" в качестве элемента списка

#Текстовое поле по-прежнему приглашает добавить еще один элемент
#Мы вводим "выпить кофе" (не зря же покупали!)

#Страница снова обнавляется, и теперь показывает оба элемента списка

#Нам интересно, запомнит ли сайт наш список.
#Здесь мы видим, что сайт сгенерировал для нас уникальный URL-адрес - об этом
#выводится небольшой текст с объяснениями

#Мы посещаем этот URL-адрес - список по-прежнему там

#На этом можно завершать тест

if __name__ == '__main__':
    unittest.main(warnings='ignore')