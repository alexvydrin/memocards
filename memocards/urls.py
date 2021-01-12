"""memocards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp  # импорт модуля views.py из приложения mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),

    # path('cards/', mainapp.cards, name='cards'),
    path('cards/', mainapp.CardsListView.as_view(), name='cards'),

    # path('cards/<int:pk>/', mainapp.card_detail, name='card_detail'),
    path('cards/<int:pk>/', mainapp.CardDetailView.as_view(), name='card_detail'),

    # path('cards/new/', mainapp.card_new, name='card_new'),
    path('cards/new/', mainapp.ClassCreateView.as_view(), name='card_new'),

    # path('cards/<int:pk>/edit/', mainapp.card_edit, name='card_edit'),
    path('cards/<int:pk>/edit/', mainapp.CardUpdateView.as_view(), name='card_edit'),

    path('cards/delete/<int:pk>/', mainapp.CardDeleteView.as_view(), name='card_delete'),

    # path('tags/', mainapp.tags, name='tags'),
    path('tags/', mainapp.TagsListView.as_view(), name='tags'),

    path('tags/<int:pk>/', mainapp.TagDetailView.as_view(), name='tag_detail'),

    path('admin/', admin.site.urls),

    path('accounts/login/', mainapp.LoginView.as_view(), name="login"),

]
