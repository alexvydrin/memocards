"""Формы"""

from django import forms
from .models import Card, Tag, CardTag


class CardForm(forms.ModelForm):
    """
    Форма для карточки
    *) эта форма пока не используется так как здесь нет специфических настроек
    """

    class Meta:
        model = Card
        fields = ('name', 'content',)


class CardTagForm(forms.ModelForm):
    """
    Форма для привязки тега к карточке
    """
    class Meta:
        fields = ['card', 'tag']
        model = CardTag

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        # Выбор возможен только среди не удаленных карточек
        self.fields['card'].queryset = Card.objects.filter(is_active=True).order_by('name')
        # Выбор возможен только среди не удаленных тегов
        self.fields['tag'].queryset = Tag.objects.filter(is_active=True).order_by('name')

    def clean(self):
        cleaned_data = super().clean()

        # Проверим запись на уникальность
        card = cleaned_data.get("card")
        tag = cleaned_data.get("tag")
        if CardTag.objects.filter(card=card, tag=tag).exists():
            raise forms.ValidationError("Такая привязка уже существует!")
