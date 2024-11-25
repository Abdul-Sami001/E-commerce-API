from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permission.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
# class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
#     def __init__(self) -> None:
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s.']