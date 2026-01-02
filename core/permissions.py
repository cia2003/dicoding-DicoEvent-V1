from rest_framework.permissions import BasePermission

class isSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
class isAdminUser(BasePermission):
    """
    Allows access only to admin users (staff).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='admin').exists()

