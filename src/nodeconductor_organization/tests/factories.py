from __future__ import unicode_literals

import factory

from rest_framework.reverse import reverse

from nodeconductor.structure.tests import factories as structure_factories
from nodeconductor_organization import models


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = models.Organization

    abbreviation = factory.Sequence(lambda n: 'TO%s' % n)
    native_name = factory.Sequence(lambda n: 'Test Organization%s' % n)
    customer = factory.SubFactory(structure_factories.CustomerFactory)

    @classmethod
    def get_url(cls, organization=None):
        if organization is None:
            organization = OrganizationFactory()
        url = 'http://testserver' + reverse('organization-detail', kwargs={'uuid': organization.uuid})
        return url

    @classmethod
    def get_list_url(self):
        return 'http://testserver' + reverse('organization-list')


class OrganizationUserFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = models.OrganizationUser

    user = factory.SubFactory(structure_factories.UserFactory)
    organization = factory.SubFactory(OrganizationFactory)

    @classmethod
    def get_url(cls, organization_user=None, action=None):
        if organization_user is None:
            organization_user = OrganizationUserFactory()
        url = 'http://testserver' + reverse('organization_user-detail',
                                            kwargs={'uuid': organization_user.uuid})
        return url if action is None else url + action + '/'

    @classmethod
    def get_list_url(self):
        return 'http://testserver' + reverse('organization_user-list')
