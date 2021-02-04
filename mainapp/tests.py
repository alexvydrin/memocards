"""Проверка работособности. Автотесты"""

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from django.contrib.auth.models import User
from mainapp.models import Card, Tag, CardTag


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
        - Привязки тегов: '/card_tag/'
        - Страница авторизации: '/accounts/login/'
        - Просмотр всех записей в БД (card, tag, card_tag)
            - Каждая карточка в БД: '/cards/{card.pk}/'
            - Каждый тег в БД: '/tags/{tag.pk}/'
            - Каждая привязка тега в БД: '/card_tag/{card_tag.pk}/'
        """

        # Сначала все пункты основного меню

        # Главная страница
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Карточки
        response = self.client.get('/cards/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи о добавлении новой карточки
        self.assertContains(response, "Добавить новую карточку")
        # В тестовой базе созданы две карточки, которые переданы для вывода на странице
        self.assertEqual(len(response.context['card_list']), 2)

        # Теги
        response = self.client.get('/tags/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи о добавлении нового тега
        self.assertContains(response, "Добавить новый тег")
        # В тестовой базе созданы два тега, которые переданы для вывода на странице
        self.assertEqual(len(response.context['tag_list']), 2)

        # Привязки тегов
        response = self.client.get('/card_tag/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи о добавлении новой привязки
        self.assertContains(response, "Добавить новую привязку")
        # В тестовой базе созданы две привязки, которые переданы для вывода на странице
        self.assertEqual(len(response.context['cardtag_list']), 2)

        # Страница авторизации
        response = self.client.get('/accounts/login/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи Вход на сайт
        self.assertContains(response, "Вход на сайт")

        # Затем просмотр всех записей в БД (card, tag)

        # Каждая карточка в БД
        for card in Card.objects.all():
            response = self.client.get(f'/cards/{card.pk}/')
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об изменении записи в БД
            self.assertContains(response, "Изменить карточку")
            # Наличие на странице надписи об удалении записи в БД
            self.assertContains(response, "Удалить карточку")

        # Каждый тег в БД
        for tag in Tag.objects.all():
            response = self.client.get(f'/tags/{tag.pk}/')
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об изменении записи в БД
            self.assertContains(response, "Изменить тег")
            # Наличие на странице надписи об удалении записи в БД
            self.assertContains(response, "Удалить тег")

        # Каждая привязку к тег в БД
        for tag in Tag.objects.all():
            response = self.client.get(f'/card_tag/{tag.pk}/')
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об изменении записи в БД
            self.assertContains(response, "Изменить привязку")
            # Наличие на странице надписи об удалении записи в БД
            self.assertContains(response, "Удалить привязку")

    def test_urls_if_logged_in(self):
        """
        Проверяем возможность открытия всех страниц,
        доступных только с авторизацией

        Сначала пытаемся открыть эти страницы без авторизации.
        Должна быть автоматическая переадресация на страницу логина

        - Страница добавления новой карточки: '/cards/new/'
        - Страница добавления нового тега: '/tags/new/'
        - Страница добавления новой привязки: '/card_tag/new/'
        - Пытаемся зайти на страницу изменения каждой карточки: '/cards/{card.pk}/edit/'
        - Пытаемся зайти на страницу удаления каждой карточки: '/cards/{card.pk}/delete/'
        - Пытаемся зайти на страницу изменения каждого тега: '/cards/{card.pk}/edit/'
        - Пытаемся зайти на страницу удаления каждого тега: '/cards/{card.pk}/delete/'
        - Пытаемся зайти на страницу изменения каждой привязки: '/card_tag/{card_tag.pk}/edit/'
        - Пытаемся зайти на страницу удаления каждой привязки: '/card_tag/{card_tag.pk}/delete/'

        Проверяем главную страницу до авторизации
        Затем логинимся
        Проверяем главную страницу после авторизации

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

        # Страница добавления новой привязки
        _path = '/card_tag/new/'
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

        # Каждая привязка в БД
        # пытаемся зайти на страницу изменения и удаления
        for card_tag in CardTag.objects.all():
            _path = f'/card_tag/{card_tag.pk}/edit/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/accounts/login/?next={_path}')
            _path = f'/card_tag/{card_tag.pk}/delete/'
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/accounts/login/?next={_path}')

        # Проверяем главную страницу ДО того как авторизировались
        response = self.client.get('/')
        self.assertContains(response, "вход")
        self.assertNotContains(response, "пользователь:")

        # Затем логинимся
        self.client.login(username=self.username, password=self.password)

        # Проверяем главную страницу ПОСЛЕ того как авторизировались
        response = self.client.get('/')
        self.assertNotContains(response, "вход")
        self.assertContains(response, f"пользователь: [{self.username}]")

        # И снова пробуем зайти на все эти страницы, но уже залогиненные

        # Страница добавления новой карточки
        _path = '/cards/new/'
        response = self.client.get(_path)
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи о добавлении записи в БД
        self.assertContains(response, "Добавление новой карточки")

        # Страница добавления нового тега
        _path = '/tags/new/'
        response = self.client.get(_path)
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи о добавлении записи в БД
        self.assertContains(response, "Добавление нового тега")

        # Страница добавления новой привязки
        _path = '/card_tag/new/'
        response = self.client.get(_path)
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице надписи о добавлении записи в БД
        self.assertContains(response, "Добавление новой привязки")

        # Каждая карточка в БД
        # пытаемся зайти на страницу изменения и удаления
        for card in Card.objects.all():
            _path = f'/cards/{card.pk}/edit/'
            response = self.client.get(_path)
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об изменении записи в БД
            self.assertContains(response, "Изменение карточки")
            _path = f'/cards/{card.pk}/delete/'
            response = self.client.get(_path)
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об удаление записи в БД
            self.assertContains(response, "Уверены, что хотите удалить")

        # Каждый тег в БД
        # пытаемся зайти на страницу изменения и удаления
        for tag in Tag.objects.all():
            _path = f'/tags/{tag.pk}/edit/'
            response = self.client.get(_path)
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об изменении записи в БД
            self.assertContains(response, "Изменение тега")
            _path = f'/tags/{tag.pk}/delete/'
            response = self.client.get(_path)
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об удаление записи в БД
            self.assertContains(response, "Уверены, что хотите удалить")

        # Каждая привязка тега в БД
        # пытаемся зайти на страницу изменения и удаления
        for card_tag in CardTag.objects.all():
            _path = f'/card_tag/{card_tag.pk}/edit/'
            response = self.client.get(_path)
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об изменении записи в БД
            self.assertContains(response, "Изменение привязки")
            _path = f'/card_tag/{card_tag.pk}/delete/'
            response = self.client.get(_path)
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице надписи об удаление записи в БД
            self.assertContains(response, "Уверены, что хотите удалить")

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
        _card_new = None
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
        _card_db.name = _name
        _card_db.content = _content
        _card_db.is_active = False
        _card_db.save()
        # Получаем ее из БД
        _card_db = None
        _card_db_2 = Card.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_card_db_2.name, _name)
        self.assertEqual(str(_card_db_2.content), _content)
        self.assertFalse(_card_db_2.is_active)

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
        _tag_new = None
        _tag_db = Tag.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_tag_db.name, _name)
        self.assertEqual(str(_tag_db), _name)  # Проверка __str__
        self.assertEqual(_tag_db.user, self.user)
        self.assertTrue(_tag_db.is_active)

        # Изменяем тег
        _name = "новый тег - изменено"
        _tag_db.name = _name
        _tag_db.is_active = False
        _tag_db.save()
        # Получаем ее из БД
        _tag_db = None
        _tag_db_2 = Tag.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_tag_db_2.name, _name)
        self.assertFalse(_tag_db_2.is_active)

    def test_card_tag(self):
        """
        CRUD CardTag
        создание, чтение, изменение
        (удаление не тестируем так как это фактически изменение поля is_active)
        """

        # Логинимся
        self.client.login(username=self.username, password=self.password)

        # Добавляем новую привязку
        _card = Card.objects.get(pk=1)
        _tag = Tag.objects.get(pk=2)
        _card_tag_new = CardTag.objects.create(
            card=_card,
            tag=_tag,
            user=self.user)
        # Получаем ее из БД
        _card_tag_new = None
        _card_tag_db = CardTag.objects.get(card=_card, tag=_tag)
        # Проверяем правильность
        self.assertEqual(_card_tag_db.card.name, _card.name)
        self.assertEqual(_card_tag_db.tag.name, _tag.name)
        _name = f"{_card.name} <--> {_tag.name}"
        self.assertEqual(str(_card_tag_db), _name)  # Проверка __str__
        self.assertEqual(_card_tag_db.user, self.user)
        self.assertTrue(_card_tag_db.is_active)

        # Изменяем привязку
        _card = Card.objects.get(pk=2)
        _tag = Tag.objects.get(pk=1)
        _card_tag_db.card = _card
        _card_tag_db.tag = _tag
        _card_tag_db.is_active = False
        _card_tag_db.save()
        # Получаем ее из БД
        _card_tag_db = None
        _card_tag_db_2 = CardTag.objects.get(card=_card, tag=_tag)
        # Проверяем правильность
        self.assertEqual(_card_tag_db_2.card.name, _card.name)
        self.assertEqual(_card_tag_db_2.tag.name, _tag.name)
        _name = f"{_card.name} <--> {_tag.name}"
        self.assertEqual(str(_card_tag_db_2), _name)  # Проверка __str__
        self.assertEqual(_card_tag_db_2.user, self.user)
        self.assertFalse(_card_tag_db_2.is_active)

    def tearDown(self):
        """Приборка после тестов"""
        # сброс индексов
        call_command('sqlsequencereset', 'mainapp')
