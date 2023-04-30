from django.conf import settings
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Title, Review
from users.models import User
from reviews.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name",
            "last_name", "bio", "role",
        )


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name",
            "last_name", "bio", "role",
        )
        read_only_fields = ("role",)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.LENG_DATA_USER,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=settings.LENG_DATA_USER,
        required=True
    )

    class Meta:
        model = User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category',
                  'genre')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение.')
        return data


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=settings.LENG_EMAIL,
        required=True,
    )
    username = serializers.CharField(
        max_length=settings.LENG_DATA_USER,
        required=True,
        validators=[validate_username],
    )


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
