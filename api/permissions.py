from rest_framework.permissions import BasePermission

class IsAuthenticatedOrGuest(BasePermission):
    
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        guest_id = request.query_params.get("guest_id")
        return bool(guest_id)  