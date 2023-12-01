from rest_framework.permissions import BasePermission


class StaffAndUsersCant(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return False
        if request.user == view.get_object().user:
            return False



class IsOwnerOrStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().user:
            return True

        if request.user.is_staff:
            return True
