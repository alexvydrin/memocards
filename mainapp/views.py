"""Контроллеры (Views)"""
from django.shortcuts import render
from .models import Card, Tag


def main(request):
    """Главная страница"""
    return render(request, 'mainapp/index.html')


def cards(request):
    """Карточки"""
    _cards = Card.objects.filter(is_active=True).order_by('name')
    return render(request, 'mainapp/card_list.html', {'cards': _cards})


def tags(request):
    """Тэги"""
    _tags = Tag.objects.filter(is_active=True).order_by('name')
    return render(request, 'mainapp/tag_list.html', {'tags': _tags})
