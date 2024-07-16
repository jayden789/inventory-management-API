from rest_framework import permissions

class IsAdminOrJWTAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow admin users to perform any operations without JWT,
    while regular users must be JWT authenticated and can only perform read operations.
    """

    def has_permission(self, request, view):
        # Admin users can perform any operations without JWT
        if request.user and request.user.is_staff:
            return True
        
        # Allow any access to read-only methods for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return False
