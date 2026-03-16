from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff
