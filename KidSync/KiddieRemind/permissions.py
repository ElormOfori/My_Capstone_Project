from rest_framework import permissions

# Check if the user owns the object (task)
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user  # True if user made it