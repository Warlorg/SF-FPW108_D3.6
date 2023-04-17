from django.http import HttpResponseRedirect
from django.shortcuts import render

from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm


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
    paginate_by = 10

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


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news_search'
    ordering = '-dateCreation'

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос.
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей.
        if not self.request.GET:
            return queryset.none()
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


def create_Post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'news_edit.html', {'form': form})


# Добавляем представление для изменения товара.
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
