from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitlesFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly, PostOnlyNoCreate)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer,
                          ReadOnlyTitleSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserSerializer, ProfileEditSerializer, SignUpSerializer, GetTokenSerializer)

##############
# EMAIL_NOREPLAY_ADDRESS = "noreplay@yamdb.team3"
#
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
# #####
#
#
# class AuthViewSet(viewsets.ModelViewSet):
#     """Получение токена авторизации JWT в ответ на POST запрос, на адрес
#     /token. POST на корневой эндпоитн и другие типы запросов запрещены
#     пермишенном."""
#
#     permission_classes = (PostOnlyNoCreate,)
#
#     @action(detail=False, methods=["post"])
#     def token(self, request):
#         """Получение токена по username и confirmation_code."""
#
#         serializer = UserConfirmCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             user = get_object_or_404(
#                 User, username=serializer.data["username"]
#             )
#             access_token = str(AccessToken.for_user(user))
#             return Response(
#                 {"access": access_token}, status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(detail=False, methods=["post"])
#     def signup(self, request):
#         """Самостоятельная регистрация нового пользователя.
#         Создает пользователя по запросу.
#         Отправляет код подверждения пользователю на email.
#         Отправляет код подверждения на email существующим пользователям."""
#
#         serializer = UserSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#         else:
#             if (
#                 "username" in serializer.data
#                 and User.objects.filter(
#                     username=serializer.data["username"],
#                     email=serializer.data["email"],
#                 ).exists()
#             ):
#                 self.send_mail_code(serializer.data)
#                 return Response(
#                     {"detail": MESSAGES["mail_send"]},
#                     status=status.HTTP_200_OK,
#                 )
#             return Response(
#                 serializer.errors, status=status.HTTP_400_BAD_REQUEST
#             )
#         self.send_mail_code(serializer.data)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             serializer.data, status=status.HTTP_200_OK, headers=headers
#         )
#
#     def send_mail_code(self, data):
#         """Функция отправки кода подтверждения."""
#
#         user = get_object_or_404(User, username=data["username"])
#         result = send_mail(
#             MESSAGES["mail_theme"],
#             MESSAGES["mail_text"].format(user.confirmation_code),
#             EMAIL_NOREPLAY_ADDRESS,
#             [data["email"]],
#             fail_silently=False,
#         )
#         return result
# ######
# class UserViewSet(viewsets.ModelViewSet):
#     """ViewSet API управления пользователями.
#     Запросы к экземпляру осуществляются по username.
#     При обращении на /me/ пользователь дополняет/получает свою запись."""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdmin,)
#     lookup_field = "username"
#
#     def retrieve(self, request, username=None):
#         """Получение экземпляра пользователя по username.
#         При запросе на /me/ возвращает авторизованного пользователя."""
#
#         if username == "me":
#             username = request.user.username
#         user = get_object_or_404(self.queryset, username=username)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def partial_update(self, request, username=None):
#         """Обновление экземпляра пользователя по username.
#         Не позволяет установить непредусмотренную роль.
#         Если пользователь не админ, не позволяет сменить роль."""
#
#         data = request.data.copy()
#         if "role" in data:
#             if data["role"] not in ("user", "admin", "moderator"):
#                 return Response(
#                     {"detail": MESSAGES["wrong_role"]},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             if not request.user.is_admin:
#                 data.pop("role")
#         serializer = UserSerializer(request.user, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
###############


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
#    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    def get_serializer_class(self):
        if (
            self.request.user.role != 'admin'
            or self.request.user.is_superuser
        ):
            return UserSerializer
        return AdminUserSerializer

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(IsAuthenticated,),
        queryset=User.objects.all()
    )
    def me(self, request):
        """
        Профиль пользователя. Можно редактировать.
        Поле role редактирует только администратор.
        """
        user = get_object_or_404(User, id=request.user.id)

        if request.method == "PATCH":
            serializer = ProfileEditSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def self_registration(request):
    if request.method == "POST":
        serializer = SignUpSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["email"] = user.email
            data["username"] = user.username
            code = default_token_generator.make_token(user)
            send_mail(
                subject="yamdb registrations",
                message=f"Пользователь {user.username} успешно зарегистрирован. Код подтверждения: {code}",
                from_email=None,
                recipient_list=[user.email],
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
    current_user_email = User.objects.get(

            username=request.data.get("username")).email

    if current_user_email != request.data["email"]:
        return Response(
                data, status=status.HTTP_400_BAD_REQUEST
            )

    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def email_verifications(request):
    serializer = GetTokenSerializer(data=request.data)
    data = {}
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"]
    )
    code = serializer.validated_data["confirmation_code"]
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        data["token"] = str(token)
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        context.update({"title": title})
        return context

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer
