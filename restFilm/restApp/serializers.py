from rest_framework import serializers
from .models import *


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListRest(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailRest(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieRest(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user', 'middle_star')


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewRest(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class ReviewListRest(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Reviews
        fields = ('name', 'text', 'children')


class MovieDetailRest(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListRest(read_only=True, many=True)
    actors = ActorListRest( read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewListRest(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingRest(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating = Rating.objects.updare_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
