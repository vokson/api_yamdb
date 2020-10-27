from rest_framework import serializers

from category.models import Categories, Genres, Titles
from django.db.models import Avg


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        # fields = '__all__'
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


# class TitlesSerializer(serializers.ModelSerializer):
#     rating = serializers.SerializerMethodField()
#     category = CategoriesSerializer(many=True, read_only=True)
#     genre = GenresSerializer(many=True, read_only=True)
#     queryset = Genres.objects.all()
#
#     class Meta:
#         model = Titles
#         fields = '__all__'
#
#     def get_rating(self, obj):
#         rating = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
#         if rating is None:
#             return 0
#         return rating


class TitleViewSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field="slug",
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field="slug",
    )

    class Meta:
        fields = '__all__'
        model = Titles
