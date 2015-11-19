from __future__ import unicode_literals

from django.db.models import Q
from rest_framework import filters as rf_filters
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from nodeconductor.structure.models import CustomerRole
from nodeconductor_organization import filters
from nodeconductor_organization import models
from nodeconductor_organization import permissions
from nodeconductor_organization import serializers


class OrganizationViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (IsAuthenticated, permissions.IsAdminOrReadOnly)
    filter_backends = (rf_filters.DjangoFilterBackend,)
    filter_class = filters.OrganizationFilter
    lookup_field = 'uuid'


class OrganizationUserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin, mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = models.OrganizationUser.objects.all()
    serializer_class = serializers.OrganizationUserSerializer
    permission_classes = (IsAuthenticated, permissions.OrganizationUserPermissions)
    filter_backends = (rf_filters.DjangoFilterBackend,)
    filter_class = filters.OrganizationUserFilter
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = super(OrganizationUserViewSet, self).get_queryset()

        if not self.request.user.is_staff:
            queryset = models.OrganizationUser.objects.filter(
                Q(user=self.request.user)
                |
                Q(organization__customer__roles__permission_group__user=self.request.user,
                  organization__customer__roles__role_type=CustomerRole.OWNER)
            )

        return queryset

    @detail_route(methods=['post'])
    def approve(self, request, uuid=None):
        instance = self.get_object()

        if instance.can_be_managed_by(request.user):
            instance.is_approved = True
            instance.save()

        return Response({'detail': "User request for joining the organization has been successfully approved"},
                        status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def reject(self, request, uuid=None):
        instance = self.get_object()

        if instance.can_be_managed_by(request.user):
            instance.is_approved = False
            instance.save()

        return Response({'detail': "User has been successfully rejected from the organization"},
                        status=status.HTTP_200_OK)
