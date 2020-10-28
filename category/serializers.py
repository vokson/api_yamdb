from rest_framework import serializers

from category.models import Categories, Genres, Titles
from django.db.models import Avg


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer_post(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta():
        fields = '__all__'
        model = Titles


class TitleSerializer_get(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta():
        fields = '__all__'
        model = Titles

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score')).get('score__avg')
