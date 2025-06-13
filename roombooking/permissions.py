from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return str(request.user) == 'admin' or str(request.user) == 'manager'