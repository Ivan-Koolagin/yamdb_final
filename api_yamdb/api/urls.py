from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       email_verifications, self_registration)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register("auth", AuthViewSet, basename="auth")
router.register("users", UserViewSet, basename="users")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", self_registration, name="self_registration"),
    path("v1/auth/token/", email_verifications, name="email_verifications"),
]
