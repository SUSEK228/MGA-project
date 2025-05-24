from rest_framework import permissions

class IsOwnerAssignedOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return (
            obj.created_by == user or
            obj.assigned_user == user or
            user.is_staff
        )
