from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from account.models import CustomUser

class TeacherPermission(permissions.BasePermission):
    """
    Custom permission to only allow non-students to access the view.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "teacher":
            return True
        return False

class StudentPermission(permissions.BasePermission):
    """
    Custom permission to only allow non-teachers to access the view.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "student":
            return True
        return False

class AdminPermission(permissions.BasePermission):
    """
    Custom permission to only allow non-teachers to access the view.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "admin":
            return True
        return False