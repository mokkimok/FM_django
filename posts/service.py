from django_filters import rest_framework as filters
from .models import Post


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter, filters.MultipleChoiceFilter):
    pass


class PostFilter(filters.FilterSet):
    """Фильтрация постов."""
    # date_added = filters.RangeFilter()
    tags = CharFilterInFilter(field_name='tags__name', lookup_expr='contains',
                              conjoined=True)

    class Meta:
        model = Post
        fields = [
            'animal_sex',
            'animal_kind',
            'post_type',
            'tags',
        ]
