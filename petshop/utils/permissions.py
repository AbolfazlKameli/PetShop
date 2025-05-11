from rest_framework.permissions import BasePermission

from petshop.users.models import User


class IsAdminUser(BasePermission):
    message = 'You dont have permission to perform this action.'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)


class NotAuthenticatedUser(BasePermission):
    message = 'You are already authenticated.'

    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)


class IsOwnerUser(BasePermission):
    message = 'You are not the owner.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj.id == request.user.id
        if hasattr(obj, 'owner') and obj.owner:
            return obj.owner.id == request.user.id
        return False


class IsOwnerOrAdminUser(BasePermission):
    message = 'You are not the owner.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        condition: bool = False
        if isinstance(obj, User):
            condition = obj.id == request.user.id
        if hasattr(obj, 'owner') and obj.owner:
            condition = obj.owner.id == request.user.id
        return condition or request.user.is_admin
