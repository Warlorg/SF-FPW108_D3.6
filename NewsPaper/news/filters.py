from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить Django дженерики.
class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='По заголовку',
    )
    post_category = CharFilter(
        field_name='postCategory__name',
        lookup_expr='icontains',
        label='По категории',
    )
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='По дате опубликования:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
        }
