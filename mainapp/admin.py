"""Регистрация моделей в админке"""
from django.contrib import admin
from .models import Card, Tag

admin.site.register(Card)
admin.site.register(Tag)
