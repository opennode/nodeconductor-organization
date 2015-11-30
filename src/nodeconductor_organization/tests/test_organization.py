from rest_framework import test
from rest_framework import status

from nodeconductor.structure import models as structure_models
from nodeconductor.structure.tests import factories as structure_factories
from nodeconductor_organization import models
from nodeconductor_organization.tests.factories import OrganizationFactory, OrganizationUserFactory


class OrganizationPermissionTest(test.APISimpleTestCase):
    def setUp(self):
        self.staff_user = structure_factories.UserFactory(is_staff=True)
        self.user = structure_factories.UserFactory()

    def tearDown(self):
        models.Organization.objects.all().delete()

    def test_anonymous_user_cannot_list_organizations(self):
        response = self.client.get(OrganizationFactory.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_organizations(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(OrganizationFactory.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_access_organization(self):
        organization = OrganizationFactory()
        self.client.force_authenticate(self.user)

        response = self.client.get(OrganizationFactory.get_url(organization))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create_organization(self):
        self.client.force_authenticate(self.user)
        data = {
            'abbreviation': 'test',
            'native_name': 'Test organization',
            'name': 'Organization'
        }

        response = self.client.post(OrganizationFactory.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_organization(self):
        self.client.force_authenticate(self.user)
        organization = OrganizationFactory()

        response = self.client.put(OrganizationFactory.get_url(organization), {'name': 'Organization2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_organization(self):
        self.client.force_authenticate(self.user)
        organization = OrganizationFactory()

        response = self.client.delete(OrganizationFactory.get_url(organization))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_create_organization(self):
        self.client.force_authenticate(self.staff_user)
        data = {
            'abbreviation': 'test',
            'native_name': 'Test organization',
            'name': 'Organization2',
            'customer': None
        }

        response = self.client.post(OrganizationFactory.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_user_can_update_organization(self):
        self.client.force_authenticate(self.staff_user)
        organization = OrganizationFactory()
        data = {
            'abbreviation': 'test',
            'native_name': 'Test organization',
            'name': 'Organization2',
            'customer': None
        }

        response = self.client.put(OrganizationFactory.get_url(organization), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_can_delete_organization(self):
        self.client.force_authenticate(self.staff_user)
        organization = OrganizationFactory()

        response = self.client.delete(OrganizationFactory.get_url(organization))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_after_removing_organization_customer_still_exist(self):
        self.client.force_authenticate(self.staff_user)
        organization = OrganizationFactory()

        response = self.client.delete(OrganizationFactory.get_url(organization))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        customer = structure_models.Customer.objects.filter(uuid=organization.customer.uuid)
        self.assertTrue(customer.exists())

    def test_after_removing_customer_organization_still_exist(self):
        self.client.force_authenticate(self.staff_user)
        organization = OrganizationFactory()

        response = self.client.delete(structure_factories.CustomerFactory.get_url(organization.customer))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        organization = models.Organization.objects.filter(uuid=organization.uuid)
        self.assertTrue(organization.exists())
        self.assertEqual(organization.first().customer, None)


class OrganizationUserPermissionTest(test.APISimpleTestCase):
    def setUp(self):
        self.customer = structure_factories.CustomerFactory()
        self.customer_owner = structure_factories.UserFactory()
        self.staff_user = structure_factories.UserFactory(is_staff=True)
        self.user = structure_factories.UserFactory()
        self.customer.add_user(self.customer_owner, structure_models.CustomerRole.OWNER)

    def tearDown(self):
        models.OrganizationUser.objects.all().delete()

    def test_anonymous_user_cannot_list_organization_users(self):
        response = self.client.get(OrganizationUserFactory.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_list_organization_users(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(OrganizationUserFactory.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_access_his_organization_user(self):
        self.client.force_authenticate(self.user)
        organization_user = OrganizationUserFactory(user=self.user)

        response = self.client.get(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_access_other_organization_users(self):
        self.client.force_authenticate(self.user)
        organization_user = OrganizationUserFactory()

        response = self.client.get(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_owner_can_access_his_customer_organization_users(self):
        organization = OrganizationFactory(customer=self.customer)
        organization_user = OrganizationUserFactory(organization=organization)

        self.client.force_authenticate(self.customer_owner)
        response = self.client.get(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_owner_cannot_access_other_customer_organization_users(self):
        self.client.force_authenticate(self.customer_owner)
        organization_user = OrganizationUserFactory()

        response = self.client.get(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_user_can_access_any_organization_user(self):
        self.client.force_authenticate(self.staff_user)
        organization_user = OrganizationUserFactory()

        response = self.client.get(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_organization_user(self):
        organization = OrganizationFactory()
        self.client.force_authenticate(self.user)
        data = {
            'user': structure_factories.UserFactory.get_url(self.user),
            'organization': OrganizationFactory.get_url(organization)
        }
        response = self.client.post(OrganizationUserFactory.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_delete_not_approved_organization_user(self):
        organization_user = OrganizationUserFactory(user=self.user)
        self.client.force_authenticate(self.user)

        response = self.client.delete(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_approved_organization_user(self):
        organization_user = OrganizationUserFactory(is_approved=True, user=self.user)
        self.client.force_authenticate(self.user)

        response = self.client.delete(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_owner_can_delete_his_customer_organization_user(self):
        organization = OrganizationFactory(customer=self.customer)
        organization_user = OrganizationUserFactory(organization=organization)
        self.client.force_authenticate(self.customer_owner)

        response = self.client.delete(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_user_can_delete_any_organization_user(self):
        organization_user = OrganizationUserFactory()
        self.client.force_authenticate(self.staff_user)

        response = self.client.delete(OrganizationUserFactory.get_url(organization_user))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Manipulation tests
    def test_user_cannot_approve_his_organization_user(self):
        self.client.force_authenticate(self.user)
        organization_user = OrganizationUserFactory(user=self.user)

        response = self.client.post(OrganizationUserFactory.get_url(organization_user,
                                                                    action='approve'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_approve_organization_user(self):
        self.client.force_authenticate(self.staff_user)
        organization_user = OrganizationUserFactory()

        response = self.client.post(OrganizationUserFactory.get_url(organization_user,
                                                                    action='approve'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization_user = models.OrganizationUser.objects.get(uuid=organization_user.uuid)
        self.assertTrue(organization_user.is_approved)

    def test_customer_owner_can_approve_his_customer_organization_user(self):
        self.client.force_authenticate(self.customer_owner)
        organization = OrganizationFactory(customer=self.customer)
        organization_user = OrganizationUserFactory(organization=organization)

        response = self.client.post(OrganizationUserFactory.get_url(organization_user,
                                                                    action='approve'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization_user = models.OrganizationUser.objects.get(uuid=organization_user.uuid)
        self.assertTrue(organization_user.is_approved)

    def test_user_cannot_reject_his_organization_user(self):
        self.client.force_authenticate(self.user)
        organization_user = OrganizationUserFactory(user=self.user, is_approved=True)

        response = self.client.post(OrganizationUserFactory.get_url(organization_user,
                                                                    action='reject'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_reject_organization_user(self):
        self.client.force_authenticate(self.staff_user)
        organization_user = OrganizationUserFactory(is_approved=True)

        response = self.client.post(OrganizationUserFactory.get_url(organization_user,
                                                                    action='reject'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization_user = models.OrganizationUser.objects.get(uuid=organization_user.uuid)
        self.assertFalse(organization_user.is_approved)

    def test_customer_owner_can_reject_his_customer_organization_user(self):
        self.client.force_authenticate(self.customer_owner)
        organization = OrganizationFactory(customer=self.customer)
        organization_user = OrganizationUserFactory(organization=organization, is_approved=True)

        response = self.client.post(OrganizationUserFactory.get_url(organization_user,
                                                                    action='reject'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization_user = models.OrganizationUser.objects.get(uuid=organization_user.uuid)
        self.assertFalse(organization_user.is_approved)
