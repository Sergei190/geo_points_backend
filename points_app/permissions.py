from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать/удалять объект только его владельцу.
    Для остальных - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        owner = getattr(obj, 'owner', None) or getattr(obj, 'author', None)
        return owner == request.user