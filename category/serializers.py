from django.db.models import Avg
from rest_framework import serializers

from category.models import Categories, Genres, Titles


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


class TitleViewSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta():
        fields = '__all__'
        model = Titles

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score')).get('score__avg')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Titles
