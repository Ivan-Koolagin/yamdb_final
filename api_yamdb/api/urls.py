from .views import (CategoryViewSet, CommentsViewSet,
                    GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet,
                    email_verifications, self_registration,
                    )
from django.urls import include, path
from rest_framework import routers



router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')

auth_patterns = [
    path('signup/', self_registration),
    path('token/', email_verifications, name="email_verifications")
]
urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router_v1.urls)),
]
