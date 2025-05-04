from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    message = 'You dont have permission to perform this action.'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)


class NotAuthenticatedUser(BasePermission):
    message = 'You are already authenticated.'

    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)
