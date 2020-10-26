from rest_framework_simplejwt import serializers

from category.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategoriesSerializer(many=True, read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
        if rating is None:
            return 0
        return rating
