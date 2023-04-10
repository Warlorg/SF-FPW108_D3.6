from django.shortcuts import render

from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import *


class AuthorsList(ListView):
    model = Author  # Указываем модель, объекты которой будут выводиться
    ordering = 'authorUser'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'authors.html'  # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'Authors'  # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'News'

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_news'] = None
        return context


class News(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'News_id'
