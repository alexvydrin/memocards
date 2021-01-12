"""Модели данных"""

from django.db import models


class Card(models.Model):
    """Карточка"""
    name = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=True)
    content = models.TextField(verbose_name='контент')
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='автор', null=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    """Тэг"""
    name = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=True)
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='автор', null=True)

    def __str__(self):
        return str(self.name)
