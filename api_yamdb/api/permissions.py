from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )
