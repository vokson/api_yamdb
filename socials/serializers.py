from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from socials.models import Review, Comment

from loguru import logger


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    # title = serializers.ReadOnlyField()

    class Meta:
        model = Review
        exclude = ('title', )
        # fields = '__all__'
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['author', 'title']
        #     )
        # ]

    # def validate(self, data):
    #     logger.debug('ReviewSerializer.validate')
        
        # author = data['author']
        # title = data['title']
        # logger.debug(title)
        # logger.debug(author)
        # if Review.objects.filter(title=title, author=author).count() > 0:
        #     raise serializers.ValidationError('Author may have only one review for title')
        # return data


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True
#     )

#     class Meta:
#         fields = ('id', 'author', 'text', 'pub_date',)
#         model = Comment
