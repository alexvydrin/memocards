"""Контроллеры (Views)"""
from django.shortcuts import redirect, render  # get_object_or_404, import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy  # import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Card, Tag  # from .forms import CardForm


def main(request):
    """Главная страница"""
    return render(request, 'mainapp/index.html')


class LoginView(TemplateView):
    """Регистрация пользователя"""
    template_name = "mainapp/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            # else:
            context['error'] = "Логин или пароль неправильные"

        return render(request, self.template_name, context)


# Card - Карточки - CBV CRUD:
# - CardListView
# - CardDetailView
# - CardCreateView
# - CardUpdateView
# - CardDeleteView


class CardListView(ListView):  # pylint: disable=too-many-ancestors
    """Просмотр списка карточек"""
    model = Card
    template_name = 'mainapp/card_list.html'

    def get_queryset(self):
        filtered_list = self.model.objects.filter(
            is_active=True).order_by('name')
        return filtered_list


class CardDetailView(DetailView):
    """Просмотр выбранной карточки"""
    model = Card
    template_name = 'mainapp/card_detail.html'


class CardCreateView(CreateView):
    """Добавление новой карточки"""
    # в версии FBV использовал форму CardForm:
    model = Card
    template_name = 'mainapp/card_edit.html'
    success_url = reverse_lazy('cards')
    fields = ['name', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление новой карточки'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardUpdateView(UpdateView):
    """Изменение карточки"""
    # в версии FBV использовал форму CardForm:
    model = Card
    template_name = 'mainapp/card_edit.html'
    success_url = reverse_lazy('cards')
    fields = ['name', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение карточки'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardDeleteView(DeleteView):
    """Удаление карточки"""
    model = Card
    template_name = 'mainapp/card_delete.html'
    success_url = reverse_lazy('cards')

    def __init__(self, *args, **kwargs):
        # self.object потом переопределим в def delete
        # (без определения всех атрибутов в __init__ ругаются линтеры)
        self.object = None
        super().__init__(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Tag - Теги - CBV CRUD:
# - TagListView
# - TagDetailView
# - TagCreateView
# - TagUpdateView
# - TagDeleteView


class TagsListView(ListView):  # pylint: disable=too-many-ancestors
    """Просмотр списка тегов"""
    model = Tag
    template_name = 'mainapp/tag_list.html'

    def get_queryset(self):
        filtered_list = self.model.objects.filter(
            is_active=True).order_by('name')
        return filtered_list


class TagDetailView(DetailView):
    """Просмотр выбранного тега"""
    model = Tag
    template_name = 'mainapp/tag_detail.html'


class TagCreateView(CreateView):
    """Добавление нового тега"""
    model = Tag
    template_name = 'mainapp/tag_edit.html'
    success_url = reverse_lazy('tags')
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление нового тега'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TagUpdateView(UpdateView):
    """Изменение тега"""
    model = Tag
    template_name = 'mainapp/tag_edit.html'
    success_url = reverse_lazy('tags')
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение тега'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TagDeleteView(DeleteView):
    """Удаление тега"""
    model = Tag
    template_name = 'mainapp/tag_delete.html'
    success_url = reverse_lazy('tags')

    def __init__(self, *args, **kwargs):
        # self.object потом переопределим в def delete
        # (без определения всех атрибутов в __init__ ругаются линтеры)
        self.object = None
        super().__init__(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
