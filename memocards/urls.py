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
    # path('', mainapp.main, name='main'),
    path('', mainapp.TagsListView.as_view(), name='main'),

    # Card - Карточки - CBV CRUD:
    path('cards/', mainapp.CardListView.as_view(), name='cards'),
    path('cards/<int:pk>/', mainapp.CardDetailView.as_view(), name='card_detail'),
    path('cards/new/', mainapp.CardCreateView.as_view(), name='card_new'),
    path('cards/<int:pk>/edit/', mainapp.CardUpdateView.as_view(), name='card_edit'),
    path('cards/<int:pk>/delete/', mainapp.CardDeleteView.as_view(), name='card_delete'),

    # Tag - Теги - CBV CRUD:
    path('tags/', mainapp.TagsListView.as_view(), name='tags'),
    path('tags/<int:pk>/', mainapp.TagDetailView.as_view(), name='tag_detail'),
    path('tags/new/', mainapp.TagCreateView.as_view(), name='tag_new'),
    path('tags/<int:pk>/edit/', mainapp.TagUpdateView.as_view(), name='tag_edit'),
    path('tags/<int:pk>/delete/', mainapp.TagDeleteView.as_view(), name='tag_delete'),

    # Привязки тега к карточке - CBV CRUD:
    path('card_tag/', mainapp.CardTagListView.as_view(), name='card_tag'),
    path('card_tag/<int:pk>/', mainapp.CardTagDetailView.as_view(), name='card_tag_detail'),
    path('card_tag/new/', mainapp.CardTagCreateView.as_view(), name='card_tag_new'),
    path('card_tag/<int:pk>/edit/', mainapp.CardTagUpdateView.as_view(), name='card_tag_edit'),
    path('card_tag/<int:pk>/delete/', mainapp.CardTagDeleteView.as_view(), name='card_tag_delete'),

    path('admin/', admin.site.urls),
    path('accounts/login/', mainapp.LoginView.as_view(), name="login"),
    # path('documentation/', mainapp.documentation, name='documentation'),
]
