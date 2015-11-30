from django.contrib import admin

from nodeconductor_organization.models import Organization, OrganizationUser


admin.site.register(Organization)
admin.site.register(OrganizationUser)
