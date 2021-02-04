"""Модели данных"""

from django.db import models


class Card(models.Model):
    """Карточка"""
    name = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=True)
    """наименование карточки"""
    content = models.TextField(verbose_name='контент')
    """контент, содержимое карточки"""
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - карточка активна
    False - карточка удалена
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания карточки"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения карточки"""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True)
    """автор карточки"""

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    """Тег"""
    name = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=True)
    """наименование тега"""
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - тег активен
    False - тег удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания тега"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения тега"""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True)
    """автор тега"""

    def __str__(self):
        return str(self.name)


class CardTag(models.Model):
    """Привязка тега к карточке"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    """карточка"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    """тег"""
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - привязка активна
    False - привязка удалена
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания привязки"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения привязки"""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True)
    """автор привязки"""

    def __str__(self):
        return f"{str(self.card.name)} <--> {str(self.tag.name)}"
