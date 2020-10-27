from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from category.models import Categories, Genres, Titles
from .permissions import IsOwnerOrReadOnly
from .permissions import IsAdminOrReadOnly
# from category.serializers import GenresSerializer, CategoriesSerializer, TitlesSerializer
from category.serializers import GenresSerializer, CategoriesSerializer, TitleViewSerializer, \
    TitlePostSerializer


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(CreateListViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


# class TitlesViewSet(ModelViewSet):
#     queryset = Titles.objects.all()
#     serializer_class = TitlesSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['category']
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    filterset_fields = ['category', 'genre', 'name', 'year']


def get_serializer_class(self):
    if self.action == 'list':
        return TitleViewSerializer
    return TitlePostSerializer
