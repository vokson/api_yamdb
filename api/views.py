import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .models import Category, Genre, Review, Title
from .permissions import IsAdminRole, RetrieveOnlyOrHasCUDPermissions, IsReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlePostSerializer, TitleViewSerializer,
                          UserSerializer, ObtainCodeSerializer, ObtainTokenSerializer)

from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_confirmation_code(request):

    serializer = ObtainCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    user, created = User.objects.get_or_create(
        email=email,
        username=username
    )

    if created:
        user.is_active = False
        user.save()

    confirmation_code = token_generator.make_token(user)

    send_mail(
        'Api YamDb - Confirmation',
        f'Your confirmation code is {confirmation_code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return Response({'email': email}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):

    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid()

    email = serializer.validated_data.get('email')
    user = get_object_or_404(User, email=email)

    confirmation_code = serializer.validated_data.get('confirmation_code')

    if not token_generator.check_token(user, confirmation_code):
        content = {'confirmation_code': ['No active account found with the given credentials']}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save()

    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    filterset_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsReadOnly | IsAdminRole | IsAdminUser]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsReadOnly | IsAdminRole | IsAdminUser]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', lookup_expr='contains')
    year = NumberFilter()

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsReadOnly | IsAdminRole | IsAdminUser]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleViewSerializer
        return TitlePostSerializer


class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [RetrieveOnlyOrHasCUDPermissions]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        author = self.request.user
        serializer.save(author=author, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [RetrieveOnlyOrHasCUDPermissions]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
