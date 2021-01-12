"""Формы"""

from django import forms
from .models import Card


class CardForm(forms.ModelForm):
    """
    Форма для карточки
    *) эта форма пока не используется так как здесь нет специфических настроек
    """

    class Meta:
        model = Card
        fields = ('name', 'content',)
