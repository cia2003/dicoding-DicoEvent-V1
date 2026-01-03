from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
class IsAdminUser(BasePermission):
    """
    Allows access only to admin users (staff).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='admin').exists()

class IsAdminOrSuperUser(BasePermission):
    """
    Allows access to admin and superusers.
    """
    def has_permission(self, request, view):
      return (
          request.user and request.user.is_authenticated and (
              request.user.is_superuser or
              request.user.groups.filter(name='admin').exists()
          )
      )
    
class IsOrganizer(BasePermission):
    """
    Allows access only to organizer users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='organizer').exists()

class IsOrganizerOrSuperUser(BasePermission):
    """
    Allows access to organizer and superusers.
    """
    def has_permission(self, request, view):
      return (
          request.user and request.user.is_authenticated and (
              request.user.is_superuser or
              request.user.groups.filter(name='organizer').exists()
          )
      )

class IsOrganizerOrAdmin(BasePermission):
    """
    Allows access to organizer and admin users.
    """
    def has_permission(self, request, view):
      return (
          request.user and request.user.is_authenticated and (
              request.user.groups.filter(name='organizer').exists() or
              request.user.groups.filter(name='admin').exists()
          )
      )