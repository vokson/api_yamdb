from django_filters.rest_framework.filters import CharFilter, NumberFilter
from django_filters.rest_framework.filterset import FilterSet
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from category.models import Categories, Genres, Titles
from category.serializers import (CategoriesSerializer, GenresSerializer,
                                  TitleSerializer_get, TitleSerializer_post)
from users.permissions import IsAdminRole

from .permissions import IsReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsReadOnly | IsAdminRole]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsReadOnly | IsAdminRole]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', lookup_expr='contains')
    year = NumberFilter()

    class Meta:
        model = Titles
        fields = ['category', 'genre', 'name', 'year']


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    # serializer_class = TitlesSerializer
    permission_classes = [IsReadOnly | IsAdminRole]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer_get
        return TitleSerializer_post
