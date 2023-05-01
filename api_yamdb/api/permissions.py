from rest_framework import permissions

class PostOnlyNoCreate(permissions.BasePermission):
    """Разрешает только метод POST. Запрещает действие метода POST create."""

    def has_permission(self, request, view):
        accept_methods = ("token", "signup")
        return request.method == "POST" and view.action in accept_methods


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )