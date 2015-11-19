from __future__ import unicode_literals

from rest_framework.permissions import BasePermission, SAFE_METHODS

from nodeconductor.structure.models import CustomerRole


class IsAdminOrReadOnly(BasePermission):
    """
    Allows full access to admin users.
    For other users read-only access.
    """

    def has_permission(self, request, view):
        user = request.user

        if user.is_staff or request.method in SAFE_METHODS:
            return True

        return False


class OrganizationUserPermissions(BasePermission):
    """
    Allows full access to admin users and organization customer owners.
    User can remove his organization user only when it is not approved.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_staff and request.method == 'DELETE':
            organization_user = view.get_object()
            if not organization_user.is_approved:
                return True

            return organization_user.can_be_managed_by(user)

        return True
