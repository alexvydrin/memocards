"""Проверка работособности. Автотесты"""

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from django.contrib.auth.models import User
from mainapp.models import Card, Tag


class TestMainappSmoke(TestCase):
    """Проверка работособности"""

    def setUp(self):
        """Предустановка, подготовка к тестам"""
        call_command('flush', '--noinput')  # очищаем тестовую базу данных
        # загружаем данные для тестов
        call_command('loaddata', 'tests_db.json')
        self.client = Client()  # объект для отправки запросов

        # Создаем юзера для тестирования
        self.username = 'test1'
        self.password = 'password_for_test'
        self.user = User.objects.create_user(
            self.username, 'test@gmail.com', self.password)
        self.user.save()

    def test_urls_if_not_logged_in(self):
        """
        Проверяем возможность открытия всех страниц,
        доступных без авторизации:

        - Главная страница: '/'
        - Карточки: '/cards/'
        - Теги: '/tags/'
        - Страница авторизации: '/accounts/login/'
        - Просмотр всех записей в БД (card, tag)
            - Каждая карточка в БД: '/cards/{card.pk}/'
            - Каждый тег в БД: '/tags/{tag.pk}/'
        """

        # Сначала все пункты основного меню

        # Главная страница
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Карточки
        response = self.client.get('/cards/')
        self.assertEqual(response.status_code, 200)

        # Теги
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, 200)

        # Страница авторизации
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        # Затем просмотр всех записей в БД (card, tag)

        # Каждая карточка в БД
        for card in Card.objects.all():
            response = self.client.get(f'/cards/{card.pk}/')
            self.assertEqual(response.status_code, 200)

        # Каждый тег в БД
        for tag in Tag.objects.all():
            response = self.client.get(f'/tags/{tag.pk}/')
            self.assertEqual(response.status_code, 200)

    def test_urls_if_logged_in(self):
        """
        Проверяем возможность открытия всех страниц,
        доступных только с авторизацией

        Сначала пытаемся открыть эти страницы без авторизации.
        Должна быть автоматическая переадресация на страницу логина

        - Страница добавления новой карточки: '/cards/new/'
        - Страница добавления нового тега: '/tags/new/'
        - Пытаемся зайти на страницу изменения каждой карточки: '/cards/{card.pk}/edit/'
        - Пытаемся зайти на страницу удаления каждой карточки: '/cards/{card.pk}/delete/'
        - Пытаемся зайти на страницу изменения каждого тега: '/cards/{card.pk}/edit/'
        - Пытаемся зайти на страницу удаления каждого тега: '/cards/{card.pk}/delete/'

        Затем логинимся

        И снова пробуем зайти на все эти страницы, но уже залогиненные
        """

        # Страница добавления новой карточки
        _path = '/cards/new/'
        response = self.client.get(_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={_path}')

        # Страница добавления нового тега
        _path = '/tags/new/'
        response = self.client.get(_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={_path}')

        # Каждая карточка в БД
        # пытаемся зайти на страницу изменения и удаления
        for card in Card.objects.all():
            _path = f'/cards/{card.pk}/edit/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/accounts/login/?next={_path}')
            _path = f'/cards/{card.pk}/delete/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/accounts/login/?next={_path}')

        # Каждый тег в БД
        # пытаемся зайти на страницу изменения и удаления
        for tag in Tag.objects.all():
            _path = f'/tags/{tag.pk}/edit/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/accounts/login/?next={_path}')
            _path = f'/tags/{tag.pk}/delete/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/accounts/login/?next={_path}')

        # Затем логинимся
        self.client.login(username=self.username, password=self.password)

        # И снова пробуем зайти на все эти страницы, но уже залогиненные

        # Страница добавления новой карточки
        _path = '/cards/new/'
        response = self.client.get(_path)
        self.assertEqual(response.status_code, 200)

        # Страница добавления нового тега
        _path = '/tags/new/'
        response = self.client.get(_path)
        self.assertEqual(response.status_code, 200)

        # Каждая карточка в БД
        # пытаемся зайти на страницу изменения и удаления
        for card in Card.objects.all():
            _path = f'/cards/{card.pk}/edit/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)
            _path = f'/cards/{card.pk}/delete/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)

        # Каждый тег в БД
        # пытаемся зайти на страницу изменения и удаления
        for tag in Tag.objects.all():
            _path = f'/tags/{tag.pk}/edit/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)
            _path = f'/tags/{tag.pk}/delete/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)

    def test_card(self):
        """
        CRUD Card

        создание, чтение, изменение

        (удаление не тестируем так как это фактически изменение поля is_active)
        """

        # Логинимся
        self.client.login(username=self.username, password=self.password)

        # Добавляем новую карточку
        _name = "новая карточка"
        _content = "Содержимое карточки"
        _card_new = Card.objects.create(
            name=_name,
            content=_content,
            user=self.user)
        # Получаем ее из БД
        _card_db = Card.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_card_db.name, _name)
        self.assertEqual(str(_card_db), _name)  # Проверка __str__
        self.assertEqual(str(_card_db.content), _content)
        self.assertEqual(_card_db.user, self.user)
        self.assertTrue(_card_db.is_active)

        # Изменяем карточку
        _name = "новая карточка - изменено"
        _content = "Содержимое карточки - изменено"
        _card_new.name = _name
        _card_new.content = _content
        _card_new.is_active = False
        _card_new.save()
        # Получаем ее из БД
        _card_db = Card.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_card_db.name, _name)
        self.assertEqual(str(_card_db.content), _content)
        self.assertFalse(_card_db.is_active)

    def test_tag(self):
        """
        CRUD Tag

        создание, чтение, изменение

        (удаление не тестируем так как это фактически изменение поля is_active)
        """

        # Логинимся
        self.client.login(username=self.username, password=self.password)

        # Добавляем новый тег
        _name = "новый тег"
        _tag_new = Tag.objects.create(
            name=_name,
            user=self.user)
        # Получаем тег из БД
        _tag_db = Tag.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_tag_db.name, _name)
        self.assertEqual(str(_tag_db), _name)  # Проверка __str__
        self.assertEqual(_tag_db.user, self.user)
        self.assertTrue(_tag_db.is_active)

        # Изменяем тег
        _name = "новый тег - изменено"
        _tag_new.name = _name
        _tag_new.is_active = False
        _tag_new.save()
        # Получаем ее из БД
        _tag_db = Tag.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_tag_db.name, _name)
        self.assertFalse(_tag_db.is_active)

    def tearDown(self):
        """Приборка после тестов"""
        # сброс индексов
        call_command('sqlsequencereset', 'mainapp')
