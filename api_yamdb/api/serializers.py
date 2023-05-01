from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title, User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

###########
# MESSAGES = {
#     "mail_send": "Email with confirmation code sent",
#     "mail_text": "Welcome!\nYour verification code YaMDB {}" "\n\nYaMDB team.",
#     "mail_theme": "YaMDB Your verification code",
#     "wrong_role": "Wrong role",
#     "no_delete_yourself": "You can't delete yourself",
#     "username_invalid": "This username is invalid",
#     "username_or_code_invalid": "Invalid username or code",
#     "duplication_review": "You have already written a review for this title",
#     "no_valid_year": "Unable to specify a year in the future",
# }
# #########
class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для админа."""
    username = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username', },
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('А username не может быть "me"')
        return value

class UserSerializer(serializers.ModelSerializer):
    # ######
    # """Сериализатор для пользователя."""
    # username = serializers.CharField(
    #     max_length=200,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # email = serializers.EmailField(
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # role = serializers.CharField(max_length=15, read_only=True)
    #
    # class Meta:
    #     fields = (
    #         'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    #     )
    #     model = User
    #     lookup_field = 'username'
    #     extra_kwargs = {
    #         'url': {'lookup_field': 'username', },
    #     }
    #     validators = (
    #         UniqueTogetherValidator(
    #         queryset=User.objects.all(),
    #         fields=['username', 'email']
    #         ),
    #         )
    #
    # def validate_username(self, value):
    #     if value == 'me':
    #         raise serializers.ValidationError('А username не может быть "me"')
    #     return value
    ####
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

#class UserSignupSerializer(serializers.ModelSerializer):
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def save(self):
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
        )
        user.save()
        return user

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                f"Использование имени {value} "
                f"в качестве username запрещено"
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100)

    class Meta:
        model = User
# class UserConfirmCodeSerializer(serializers.Serializer):
#     "Сериалайзер для проверки username с кодом подтверждения."
#     username = serializers.CharField(max_length=150, required=True)
#     confirmation_code = serializers.CharField(max_length=64, required=True)
#
#     def validate(self, data):
#         """Проверка соответстствия кода логину."""
#         user = get_object_or_404(User, username=data["username"])
#         if user.confirmation_code == data["confirmation_code"]:
#             return data
#         raise serializers.ValidationError(MESSAGES["username_or_code_invalid"])
#

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError("Only one review is allowed")
        return data

    class Meta:
        fields = ("id", "author", "title", "text", "pub_date", "score")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)

    class Meta:
        fields = ("id", "author", "review", "text", "pub_date")
        model = Comment


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source="reviews__score__avg", read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
